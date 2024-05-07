import Link from "next/link";
import Layout from "../frontend/components/Layout";

function HomePage() {
  return (
    <Layout>
      <h1>Welcome to our e-commerce website!</h1>
      <Link href="/products">View our products</Link>
    </Layout>
  );
}

export default HomePage;
