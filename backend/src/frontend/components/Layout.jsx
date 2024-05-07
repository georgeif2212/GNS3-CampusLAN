// components/Layout.js
import React from 'react';
import Aside from './Aside.jsx';
import Header from './Header.jsx';
import styles from '../styles/layouts/layout.module.scss'

const Layout = ({ children }) => {
  return (
    <div className={styles.layout}>
      <Header/>
      <div className={styles.content}>
        <Aside/>
        <main className={styles.main_content}>{children}</main>
      </div>
    </div>
  );
};

export default Layout;
