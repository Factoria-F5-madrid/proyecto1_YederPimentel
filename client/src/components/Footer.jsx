// src/components/Footer.jsx
function Footer() {
  return (
    <footer className="bg-gray-100 text-center text-gray-600 py-4 mt-10">
      © {new Date().getFullYear()} TaxiMeter · Todos los derechos reservados.
    </footer>
  );
}

export default Footer;
