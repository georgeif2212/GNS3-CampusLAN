import Link from "next/link";

function HomePage() {
  return (
    <div>
      <h1>Welcome to our e-commerce website!</h1>
      <Link href="/products">View our products</Link> {/* Sin `<a>` */}
    </div>
  );
}

export default HomePage;
