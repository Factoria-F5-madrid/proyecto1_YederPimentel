function Footer() {
  return (
    <footer className="bg-blue-900 text-center text-sm text-white py-4 mt-auto">
      <div className="max-w-6xl mx-auto px-4">
        © {new Date().getFullYear()}{" "}
        <span className="font-semibold">TaxiMeter F5</span> · Todos los derechos
        reservados.
      </div>
    </footer>
  );
}

export default Footer;
