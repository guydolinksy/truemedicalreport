import './App.css';
import React, {useEffect} from "react";
import {ConfigProvider, Layout} from 'antd';
import {LoginProvider} from "./components/LoginContext";
import {BrowserRouter as Router, generatePath, Route, Routes, Navigate} from 'react-router-dom';
import {WING_URL, WingView} from "./pages/WingView";
import {LOGIN_URL, LoginView} from "./pages/LoginView";
import {DEPARTMENT_URL, DepartmentView} from "./pages/DepartmentView";
import {useMatomo} from "@datapunt/matomo-tracker-react";
import {UserTheme} from "./themes/ThemeContext";
import {HashMatch} from "./components/HashMatch";
import {TimeContextProvider} from "./components/RelativeTime";
import {MAIN_URL, MainView} from "./pages/MainView";

function App() {
    const {trackPageView} = useMatomo();

    useEffect(() => {
        trackPageView();
    }, [])

    return (
        <ConfigProvider direction={"rtl"}>
            <TimeContextProvider>
                <div className={"App"} style={{backgroundColor: "#dcdcdc"}} dir={"rtl"}>
                    <Router>
                        <HashMatch>
                            <LoginProvider>
                                {({user}) =>
                                    <UserTheme>
                                        <Routes>
                                            <Route path={LOGIN_URL} element={<LoginView/>}/>
                                            <Route element={<MainView/>}>
                                                <Route path={DEPARTMENT_URL} element={<DepartmentView/>}>
                                                    <Route path={WING_URL} element={<WingView/>}/>
                                                </Route>
                                                <Route path={'*'} element={<Navigate to={MAIN_URL}/>}/>
                                            </Route>
                                        </Routes>
                                    </UserTheme>
                                }
                            </LoginProvider>
                        </HashMatch>
                    </Router>
                </div>
            </TimeContextProvider>
        </ConfigProvider>
    );
}

export default App;
