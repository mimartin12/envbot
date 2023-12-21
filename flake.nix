{
  description = "Pluggable Slack Bot POC";
  inputs = { nixpkgs.url = "github:nixos/nixpkgs/22.11"; };

  outputs = { self, nixpkgs, flake-utils}: 
    flake-utils.lib.eachDefaultSystem (system: 
      let
        #pkgs = nixpkgs.legacyPackages.x86_64-linux.pkgs;
        pkgs = nixpkgs.legacyPackages.${system};
        packageName = "BDB-1";
      in {
        devShells.default = pkgs.mkShell {
          name = "${packageName}";
          buildInputs = [
            pkgs.pipenv
            pkgs.python311
          ];
          shellHook = ''
            echo "Welcome in $name"
            export PS1="\[\e[1;33m\][nix(bdb-1)]\$\[\e[0m\] "
          '';
        };
      }
    );
}
