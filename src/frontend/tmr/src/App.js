import './App.css';
import React from 'react-dom'
import {ConfigProvider, Layout} from 'antd';
import {LoginProvider} from "./components/LoginContext";
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import {WING_URL, WingView} from "./pages/WingView";
import {LOGIN_URL, LoginView} from "./pages/LoginView";
import {DEPARTMENT_URL, DepartmentView} from "./pages/DepartmentView";
import {SETTINGS_URL, SettingsView} from "./pages/SettingsView";

function App() {
    return (
        <ConfigProvider direction={"rtl"}>
            <div className={"App"} style={{backgroundColor: "#dcdcdc"}} dir={"rtl"}>
                <Router>
                    <LoginProvider>
                        {({user}) =>
                            <Layout style={{height: '100vh'}}>
                                <Routes>
                                    <Route path={LOGIN_URL} element={<LoginView/>}/>
                                    <Route path={WING_URL} element={<WingView/>}/>
                                    <Route path={DEPARTMENT_URL} element={<DepartmentView/>}/>
                                    <Route path={SETTINGS_URL} element={<SettingsView/>}/>
                                </Routes>
                            </Layout>
                        }
                    </LoginProvider>
                </Router>
            </div>
        </ConfigProvider>
    );
}

export default App;
