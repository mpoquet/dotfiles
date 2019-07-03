{   pkgs ? import (
      fetchTarball "https://github.com/NixOS/nixpkgs/archive/19.03.tar.gz") {}
}:

pkgs.mkShell rec {
  buildInputs = with pkgs.python37Packages; [
    pkgs.python37
    docopt
  ];
}
