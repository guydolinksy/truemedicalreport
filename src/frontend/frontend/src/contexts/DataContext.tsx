import type { FC, ReactElement } from 'react';
import { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import type { AxiosError } from 'axios';
import Axios from 'axios';
import useWebSocket from 'react-use-websocket';
import debounce from 'lodash/debounce';
import { notification } from 'antd';

interface IProviderValue<T> {
  value?: T;
  update: (path: string[], newValue: any, type: string) => void;
  loading: boolean;
  flush: () => void;
  lastMessage?: unknown;
}

type ChildrenProps<T, U extends {} = {}> = U & Omit<IProviderValue<T>, 'loading'>;

interface IProviderProps<T, U extends {} = {}> {
  url: string;
  updateURL?: string;
  socketURL?: never;
  defaultValue?: T;
  onError?: (error: AxiosError) => void;
  children: (props: ChildrenProps<T, U>) => ReactElement;
}

type ProviderProps<T, U extends {} = {}> = IProviderProps<T, U> & U;

export const createDataContext = <T, U extends {} = {}>() => {
  const context = createContext<IProviderValue<T>>(null as unknown as IProviderValue<T>);

  const Provider: FC<ProviderProps<T, U>> = ({
    url,
    updateURL,
    socketURL,
    defaultValue = undefined,
    onError,
    ...props
  }) => {
    const [{ loading, value }, setValue] = useState({ loading: true, value: defaultValue });

    // When the website is served over HTTPs, the browser blocks non-TLS websocket connections.
    const websocketScheme = window.location.protocol.startsWith('https') ? 'wss' : 'ws';

    const { lastJsonMessage } = useWebSocket(`${websocketScheme}://${window.location.host}/api/sync/ws`, {
      share: true,
      shouldReconnect: () => true,
      retryOnError: true,
      onReconnectStop: (e) => {
        console.log('reconnect', e);
        notification.error({
          duration: 10,
          message: 'שגיאה בעדכון נתונים',
          description: 'המידע המוצג אינו מתעדכן עקב שגיאת חיבור, יש לרענן את העמוד.',
        });
      },
    });

    const flush = useMemo(
      () =>
        debounce(
          () => {
            const cancellationSource = Axios.CancelToken.source();
            Axios.get(url, { cancelToken: cancellationSource.token })
              .then((response) => {
                setValue({ loading: false, value: response.data });
              })
              .catch((error) => {
                if (Axios.isCancel(error)) return;
                if (onError) onError(error);
                console.error(error);
              });

            return () => cancellationSource.cancel();
          },
          1000,
          { leading: true, trailing: true },
        ),
      [url, onError],
    );

    useEffect(() => {
      return flush();
    }, [url, flush]);

    useEffect(() => {
      if (lastJsonMessage && lastJsonMessage.keys.includes(url)) {
        flush();
      }
    }, [lastJsonMessage, url, flush]);

    const update = useCallback(
      (path: string[], newValue: any, type: string) => {
        const deepReplace = (path: string[], data: any, value: any): any => {
          if (!path.length) {
            return value;
          }
          const key = path.pop();
          return Object.assign({}, data, {
            [key as string]: deepReplace(path, data[key as string], value),
          });
        };
        setValue((prevState) => {
          const newData = deepReplace(path.slice().reverse(), prevState.value, newValue);
          Axios.post(updateURL || url, { data: newData, path: path, value: newValue, type_: type }).catch((error) => {
            console.error('update error', error);
          });
          return { loading: prevState.loading, value: newData };
        });
      },
      [url, updateURL],
    );

    return (
      <context.Provider
        value={{
          value: value,
          update: update,
          loading: loading,
          flush: flush,
        }}
      >
        {!loading && props.children?.({ value: value, update: update, flush: flush, ...props } as ChildrenProps<T, U>)}
      </context.Provider>
    );
  };

  const withData =
    (Component: FC<U & IProviderValue<T>>) =>
    ({ ...props }: U) => {
      return (
        <context.Consumer>
          {({ value, update, loading, flush, lastMessage }) => (
            <Component
              loading={loading}
              value={value}
              update={update}
              flush={flush}
              lastMessage={lastMessage}
              {...props}
            />
          )}
        </context.Consumer>
      );
    };

  return { withData: withData, Provider: Provider, context: context };
};
