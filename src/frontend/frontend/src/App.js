import './App.css';
import React, { useEffect } from 'react';
import { ConfigProvider } from 'antd';
import { LoginProvider } from './components/LoginContext';
import { BrowserRouter as Router, Navigate, Route, Routes } from 'react-router-dom';
import { LOGIN_URL, LoginView } from './pages/LoginView';
import { useMatomo } from '@datapunt/matomo-tracker-react';
import { UserTheme } from './themes/ThemeContext';
import { HashMatch } from './components/HashMatch';
import { TimeContextProvider } from './components/RelativeTime';
import { MAIN_URL, MainView } from './pages/MainView';
import { ModeProvider } from './contexts/ModeContext';
import { INFO_URL, InfoView } from './pages/InfoView';
import { DEFAULT_MODE_URL, DefaultModeForView, MODE_URL, ModeView } from './pages/ModeView';
import { HOME_URL, HomeView } from './pages/HomeView';
import { VIEWS_URL, ViewsView } from './pages/ViewsView';

function App() {
  const { trackPageView } = useMatomo();

  useEffect(() => {
    trackPageView();
  }, []);

  return (
    <ConfigProvider direction={'rtl'}>
      <TimeContextProvider>
        <ModeProvider>
          <div className={'App'} style={{ backgroundColor: '#dcdcdc' }} dir={'rtl'}>
            <Router>
              <HashMatch>
                <LoginProvider>
                  {({ user }) => (
                    <UserTheme>
                      <Routes>
                        <Route path={LOGIN_URL} element={<LoginView />} />
                        <Route element={<MainView />}>
                          <Route exact path={HOME_URL} element={<HomeView />} />
                          <Route exact path={VIEWS_URL} element={<ViewsView />} />
                          <Route path={MODE_URL} element={<ModeView />}>
                            <Route path={INFO_URL} element={<InfoView />} />
                          </Route>
                          <Route path={DEFAULT_MODE_URL} element={<DefaultModeForView />} />
                        </Route>
                        <Route path={'*'} element={<Navigate to={MAIN_URL} />} />
                      </Routes>
                    </UserTheme>
                  )}
                </LoginProvider>
              </HashMatch>
            </Router>
          </div>
        </ModeProvider>
      </TimeContextProvider>
    </ConfigProvider>
  );
}

export default App;
