import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import taaxiBackground from "../assets/taxi.jpg";

const Layout = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      {/* en el main quiero poner el taxibackground */}
      <main
        className="flex-grow flex items-center justify-center"
        style={{
          backgroundImage: `url(${taaxiBackground})`,
          backgroundPosition: "center top",
          backgroundRepeat: "no-repeat",
          backgroundSize: "100% auto",
        }}
      >
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
