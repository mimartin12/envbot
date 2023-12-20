{
  description = "Pluggable Slack Bot POC";
  inputs = { nixpkgs.url = "github:nixos/nixpkgs/22.11"; };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux.pkgs;
    in {
      devShells.x86_64-linux.default = pkgs.mkShell {
        name = "BDB-1";
        buildInputs = [
          pkgs.pipenv
          pkgs.python311
        ];
        shellHook = ''
          echo "Welcome in $name"
          export PS1="\[\e[1;33m\][nix(bdb-1)]\$\[\e[0m\] "
        '';
      };
    };
}
