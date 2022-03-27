import './App.css';
import {Wing} from './components/Wing'
import {ConfigProvider, Layout} from 'antd';

const {Header, Content} = Layout;

function App() {
    const wingId = 0;
    return (
        <ConfigProvider direction="rtl">
            <div className="App" style={{backgroundColor: "#dcdcdc"}} dir={"rtl"}>
                <Layout>
                    <Header>

                    </Header>
                    <Content>
                        <Wing wingId={wingId} />
                    </Content>
                </Layout>
            </div>
        </ConfigProvider>
    );
}

export default App;
