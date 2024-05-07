import Link from "next/link";
import styles from "../styles/layouts/aside.module.scss";

const Aside = () => {
  return (
    <aside className={styles.aside}>
      <ul>
        <li>
          <Link href="/settings">Settings</Link>
        </li>
        <li>
          <Link href="/statistics">Statistics</Link>
        </li>
        <li>
          <Link href="/logs">Logs</Link>
        </li>
      </ul>
    </aside>
  );
};

export default Aside;
