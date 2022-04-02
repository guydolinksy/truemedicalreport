import './App.css';
import React from 'react-dom'
import {ConfigProvider, Layout} from 'antd';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import {WingView, WING_URL} from "./pages/WingView";
import {DepartmentView, DEPARTMENT_URL} from "./pages/DepartmentView";

const {Header, Content} = Layout;

function App() {
    return (
        <ConfigProvider direction="rtl">
            <div className="App" style={{backgroundColor: "#dcdcdc"}} dir={"rtl"}>
                <Router>
                    <Layout style={{height: '100vh'}}>
                        <Routes>
                            <Route path={WING_URL} element={<WingView/>}/>
                            <Route path={DEPARTMENT_URL} element={<DepartmentView/>}/>
                        </Routes>
                    </Layout>
                </Router>
            </div>
        </ConfigProvider>
    );
}

export default App;
