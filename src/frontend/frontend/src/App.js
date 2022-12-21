import './App.css';
import React, {useEffect} from "react";
import {ConfigProvider, Layout} from 'antd';
import {LoginProvider} from "./components/LoginContext";
import {BrowserRouter as Router, generatePath, Route, Routes} from 'react-router-dom';
import {Navigate} from 'react-router';
import {WING_URL, WingView} from "./pages/WingView";
import {LOGIN_URL, LoginView} from "./pages/LoginView";
import {DEPARTMENT_URL, DepartmentView} from "./pages/DepartmentView";
import {SETTINGS_URL, SettingsView} from "./pages/SettingsView";
import {useMatomo} from "@datapunt/matomo-tracker-react";
import {UserTheme} from "./themes/ThemeContext";
import {HashMatch} from "./components/HashMatch";
import {TimeContextProvider} from "./components/RelativeTime";
import * as Sentry from "@sentry/browser";

function App() {
    Sentry.init({
        dsn: "http://b85e67e9bf1d488f9e633739f487f780@localhost:9000/4"
    });

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
                                        <Layout style={{height: '100vh'}}>
                                            <Routes>
                                                <Route path={LOGIN_URL} element={<LoginView/>}/>
                                                <Route path={WING_URL} element={<WingView/>}/>
                                                <Route path={DEPARTMENT_URL} element={<DepartmentView/>}/>
                                                <Route path={SETTINGS_URL} element={<SettingsView/>}/>
                                                <Route path={'*'} element={<Navigate to={generatePath(
                                                    DEPARTMENT_URL, {department: (user && user.department) || "er"}
                                                )}/>}/>
                                            </Routes>
                                        </Layout>
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
