import {useLocation} from "react-router";

export const HashMatch = ({match, ...props}) => {
    const {hash} = useLocation(), parts = hash.split('#').slice(1);
    const matched = parts.length >= match.length && !match.some((m, i) => parts[i] !== m);
    return props.children({matched: matched, match: matched ? parts.slice(match.length) : [], ...props})
}