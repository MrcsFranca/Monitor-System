{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (ps:
      with ps; [
        grpcio
        grpcio-tools
        psutil
      ]))
  ];
}
