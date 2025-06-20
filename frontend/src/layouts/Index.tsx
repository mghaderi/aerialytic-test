import React from 'react';
import Header from '../components/Header';

// Layout component wraps the app content with a consistent structure (Header + Main)
const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div className="App">
        <Header />
        <main>{children}</main>
    </div>
);

export default Layout;
