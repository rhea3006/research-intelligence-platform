type NavbarProps = {

  title: string;

  subtitle: string;

};

function Navbar({ title, subtitle }: NavbarProps) {

  return (

    <nav>

      <h2>{title}</h2>

      <p>{subtitle}</p>

    </nav>

  );

}

export default Navbar;