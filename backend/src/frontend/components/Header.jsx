import Link from 'next/link';
import styles from'../styles/layouts/header.module.scss'

const Header = () => {
  return (
    <header className={styles.header}>
      <h1>Dashboard</h1>
      <nav>
        <ul>
          <li>
            <Link href="/home">Home</Link>
          </li>
          <li>
            <Link href="/products">Products</Link>
          </li>
          <li>
            <Link href="/reports">Reports</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
