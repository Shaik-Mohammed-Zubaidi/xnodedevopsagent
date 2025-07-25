import React from 'react';
import './App.css';
import { Flex, Layout } from 'antd';
import MainPage from './MainPage';


const { Header, Footer, Sider, Content } = Layout;

const headerStyle = {
  textAlign: 'center',
  color: '#fff',
  height: 64,
  paddingInline: 48,
  lineHeight: '64px',
  backgroundColor: '#4096ff',
  fontSize: 24,
};
const contentStyle = {
  textAlign: 'center',
  // minHeight: 120,
  height: '90vh',
  // lineHeight: '120px',
  // color: '#fff',
  // backgroundColor: '#0958d9',
};
// const siderStyle = {
//   textAlign: 'center',
//   lineHeight: '120px',
//   color: '#fff',
//   backgroundColor: '#1677ff',
// };
const footerStyle = {
  textAlign: 'center',
  color: '#fff',
  backgroundColor: '#4096ff',
};
const layoutStyle = {
  borderRadius: 8,
  overflow: 'hidden',
  width: 'calc(50% - 8px)',
  maxWidth: 'calc(50% - 8px)',
};
const App = () => (
  <Flex gap="middle" wrap>
    <Layout >
      <Header style={headerStyle} > Devops ReAct Agent</Header>
      <Content style={contentStyle}>
        <MainPage />
      </Content>
    </Layout>
  </Flex>
);
export default App;