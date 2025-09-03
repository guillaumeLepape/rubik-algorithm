from pydantic import BaseModel, computed_field


class Move(BaseModel):
    notation: str
    description: str


class Algorithm(BaseModel):
    name: str
    moves: list[str]
    image_url: str


class AlgorithmGroup(BaseModel):
    description: str
    algorithms: list[Algorithm]


class F2LAlgorithms(BaseModel):
    title: str
    groups: list[AlgorithmGroup]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def description(self) -> str:
        return (
            "Solve the first two layers of the cube simultaneously with these intuitive algorithms."
        )


class OLLAlgorithms(BaseModel):
    title: str
    groups: list[AlgorithmGroup]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def description(self) -> str:
        total_groups = len(self.groups)
        total_algorithms = sum(len(group.algorithms) for group in self.groups)

        return (
            f"Orient all pieces on the last layer. Master these {total_algorithms} algorithms "
            f"spread across {total_groups} groups."
        )


class PLLAlgorithms(BaseModel):
    title: str
    groups: list[AlgorithmGroup]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def description(self) -> str:
        total_groups = len(self.groups)
        total_algorithms = sum(len(group.algorithms) for group in self.groups)

        return (
            "Permute the last layer pieces to their final positions with these "
            f"{total_algorithms} algorithms spread across {total_groups} groups."
        )


class COFPAlgorithms(BaseModel):
    f2l: F2LAlgorithms
    oll: OLLAlgorithms
    pll: PLLAlgorithms


COFP_ALGORITHMS = COFPAlgorithms(
    f2l=F2LAlgorithms(
        title="F2L (First Two Layers)",
        groups=[
            AlgorithmGroup(
                description="Connected Pairs",
                algorithms=[
                    Algorithm(
                        name="Corner up, edge in top layer",
                        moves=["R U' R' F R F'"],
                        image_url="test",
                    )
                ],
            )
        ],
    ),
    oll=OLLAlgorithms(
        title="OLL (Orient Last Layer)",
        groups=[
            AlgorithmGroup(
                description="All edges flipped correctly",
                algorithms=[
                    Algorithm(
                        name="OLL 27",
                        moves=["R U R' U R U2 R'", "y' R' U2 R U R' U R"],
                        image_url="/static/oll/O27.png",
                    ),
                    Algorithm(
                        name="OLL 26",
                        moves=["y2 R' U' R U' R' U2 R"],
                        image_url="/static/oll/O26.png",
                    ),
                    Algorithm(
                        name="OLL 21",
                        moves=["R U R' U R U' R' U R U2 R'", "y F (R U R' U')3 F'"],
                        image_url="/static/oll/O21.png",
                    ),
                    Algorithm(
                        name="OLL 22",
                        moves=["R U2 R2' U' R2 U' R2' U2 R"],
                        image_url="/static/oll/O22.png",
                    ),
                    Algorithm(
                        name="OLL 23",
                        moves=["R2 D' R U2 R' D R U2 R", "(y2) R2 D R' U2 R D' R' U2 R'"],
                        image_url="/static/oll/O23.png",
                    ),
                    Algorithm(
                        name="OLL 24",
                        moves=["r U R' U' r' F R F'", "(y' x') R U R' D R U' R' D'"],
                        image_url="/static/oll/O24.png",
                    ),
                    Algorithm(
                        name="OLL 25",
                        moves=["y' F' r U R' U' r' F R", "l' U' L' U R U' L U x'"],
                        image_url="/static/oll/O25.png",
                    ),
                ],
            ),
            AlgorithmGroup(
                description="No edges flipped correctly",
                algorithms=[
                    Algorithm(
                        name="OLL 1",
                        moves=["R U2 R2 F R F' U2 R' F R F'"],
                        image_url="/static/oll/O1.png",
                    ),
                    Algorithm(
                        name="OLL 2",
                        moves=[
                            "F (R U R' U') F' f (R U R' U') f'",
                            "(y) (r U r') U2 R U2 R' U2 (r U' r')",
                        ],
                        image_url="/static/oll/O2.png",
                    ),
                    Algorithm(
                        name="OLL 3",
                        moves=[
                            "(y') f (R U R' U') f' U' F (R U R' U') F'",
                            "(y) r' R2 U R' U r U2 r' U R' r",
                        ],
                        image_url="/static/oll/O3.png",
                    ),
                    Algorithm(
                        name="OLL 4",
                        moves=["f (R U R' U') f' U F (R U R' U') F'"],
                        image_url="/static/oll/O4.png",
                    ),
                    Algorithm(
                        name="OLL 17",
                        moves=["R U R' U (R' F R F') U2 (R' F R F')"],
                        image_url="/static/oll/O17.png",
                    ),
                    Algorithm(
                        name="OLL 18",
                        moves=["R U2 R2 F R F' U2 M' U R U' r'"],
                        image_url="/static/oll/O18.png",
                    ),
                    Algorithm(
                        name="OLL 19",
                        moves=["r' R U (R U R' U') r R2' F R F'"],
                        image_url="/static/oll/O19.png",
                    ),
                ],
            ),
            AlgorithmGroup(
                description='"P" shapes',
                algorithms=[
                    Algorithm(
                        name="OLL 31",
                        moves=["(y2) R' U' F (U R U' R') F' R"],
                        image_url="/static/oll/O31.png",
                    ),
                    Algorithm(
                        name="OLL 32",
                        moves=["R U B' U' R' U R B R'", "S (R U R' U') (R' F R f')"],
                        image_url="/static/oll/O32.png",
                    ),
                    Algorithm(
                        name="OLL 43",
                        moves=["(y) R' U' F' U F R", "(y2) F' (U' L' U L) F"],
                        image_url="/static/oll/O43.png",
                    ),
                    Algorithm(
                        name="OLL 44",
                        moves=["f (R U R' U') f'", "(y2) F (U R U' R') F'"],
                        image_url="/static/oll/O44.png",
                    ),
                ],
            ),
            AlgorithmGroup(
                description="OLL 36",
                algorithms=[
                    Algorithm(
                        name="OLL 36",
                        moves=[
                            "(y2) (L' U' L U') (L' U L U) (L F' L' F)",
                            "(y) R U R2 F' U' F U R2 U2 R'",
                        ],
                        image_url="/static/oll/O36.png",
                    ),
                    Algorithm(
                        name="OLL 38",
                        moves=["(y2) (R U R' U) (R U' R' U') (R' F R F')"],
                        image_url="/static/oll/O38.png",
                    ),
                ],
            ),
            AlgorithmGroup(
                description='"L" shapes',
                algorithms=[
                    Algorithm(
                        name="OLL 48",
                        moves=["F (R U R' U') (R U R' U') F'"],
                        image_url="/static/oll/O48.png",
                    ),
                    Algorithm(
                        name="OLL 47",
                        moves=["F' (L' U' L U) (L' U' L U) F", "R' U' (R' F R F') (R' F R F') U R"],
                        image_url="/static/oll/O47.png",
                    ),
                    Algorithm(
                        name="OLL 53",
                        moves=["(y2) r' U' (R U' R') (U R U' R') U2 r"],
                        image_url="/static/oll/O53.png",
                    ),
                    Algorithm(
                        name="OLL 54",
                        moves=["r U R' (U R U' R') U R U2 r'"],
                        image_url="/static/oll/O54.png",
                    ),
                    Algorithm(
                        name="OLL 49",
                        moves=["(y2) r U' r2 U r2 U r2 U' r"],
                        image_url="/static/oll/O49.png",
                    ),
                    Algorithm(
                        name="OLL 50",
                        moves=["r' U r2 U' r2' U' r2 U r'"],
                        image_url="/static/oll/O50.png",
                    ),
                ],
            ),
            AlgorithmGroup(
                description='"C" shapes',
                algorithms=[
                    Algorithm(
                        name="OLL 34",
                        moves=["(R U R' U') B' (R' F R S) z'", "(R U R2 U') R' F R U R U' F'"],
                        image_url="/static/oll/O34.png",
                    ),
                    Algorithm(
                        name="OLL 46",
                        moves=["R' U' (R' F R F') U R"],
                        image_url="/static/oll/O46.png",
                    ),
                ],
            ),
        ],
    ),
    pll=PLLAlgorithms(
        title="PLL (Permute Last Layer)",
        groups=[
            AlgorithmGroup(
                description="Permutations of Edges Only",
                algorithms=[
                    Algorithm(
                        name="H permutation",
                        moves=[
                            "M2' U M2' U2 M2' U M2'",
                            "M2' U' M2' U2' M2' U' M2'",
                            "R2' U2 R' U2 R2' U2' R2' U2 R' U2 R2'",
                        ],
                        image_url="/static/pll/H.webp",
                    ),
                    Algorithm(
                        name="U permutation : a",
                        moves=[
                            "(y2) R U' R U R U R U' R' U' R2",
                            "R U R' U R' U' R2 U' R' U R' U R",
                        ],
                        image_url="/static/pll/U1.webp",
                    ),
                    Algorithm(
                        name="U permutation : b",
                        moves=["(y2) M2 U' M U2 M' U' M2", "R' U R' U' R3 U' R' U R U R2"],
                        image_url="/static/pll/U.webp",
                    ),
                    Algorithm(
                        name="Z permutation",
                        moves=["(y) M2' U2 M U M2' U M2' U M", "M2' U2 M U' M2' U' M2' U' M"],
                        image_url="/static/pll/Z.webp",
                    ),
                ],
            ),
            AlgorithmGroup(
                description="Permutations of Corners Only",
                algorithms=[
                    Algorithm(
                        name="A permutation : a",
                        moves=[
                            "(x) R' U R' D2 R U' R' D2 R2 (x')",
                            "l' U R' D2 R U' R' D2 R2 (x')",
                            "(y) R' D' R U' R' D R U2 R' D' R U' R' D R",
                        ],
                        image_url="/static/pll/A1.webp",
                    ),
                    Algorithm(
                        name="A permutation : b",
                        moves=[
                            "(y' x) R2 D2 R U R' D2 R U' R (x')",
                            "(y') R' D' R U R' D R U R' D' R U2 R' D R",
                        ],
                        image_url="/static/pll/A.webp",
                    ),
                    Algorithm(
                        name="E permutation",
                        moves=[
                            "(y x') (R U' R' D) (R U R' D') (R U R' D) (R U' R' D') (x)",
                            "R2 U R' U' (y) (R U R' U')2 R U R' (y') R U' R2'",
                        ],
                        image_url="/static/pll/E.webp",
                    ),
                ],
            ),
            AlgorithmGroup(
                description="Permutations of Edges and Corners",
                algorithms=[
                    Algorithm(
                        name="F permutation",
                        moves=[
                            "(y) R' U' F' (R U R' U') R' F R2 (U' R' U') R U R' U R",
                            "(y2) R' U2 R' d' R' F' R2 U' R' U R' F R U' F",
                        ],
                        image_url="/static/pll/F.webp",
                    ),
                    Algorithm(
                        name="G permutation : a",
                        moves=["(y) R2 U (R' U R' U') R U' R2 (D U' R' U) R D'"],
                        image_url="/static/pll/G3.webp",
                    ),
                    Algorithm(
                        name="G permutation : b",
                        moves=["R' U' R U D' R2 U R' U R U' R U' R2 D"],
                        image_url="/static/pll/G2.webp",
                    ),
                    Algorithm(
                        name="G permutation : c",
                        moves=[
                            "(y) R2 U' R U' R U R' U R2 D' U R U' R' D",
                            "(y') R2 F2 R U2 R U2 R' F R U R' U' R' F R2",
                        ],
                        image_url="/static/pll/G1.webp",
                    ),
                    Algorithm(
                        name="G permutation : d",
                        moves=[
                            "(y2) R U R' U' D R2 U' R U' R' U R' U R2 D'",
                            "(y2) D' R U R' U' D R2 U' R U' R' U R' U R2",
                        ],
                        image_url="/static/pll/G4.webp",
                    ),
                    Algorithm(
                        name="J permutation : a",
                        moves=["(y2) x R2' F R F' R U2 r' U r U2 x'"],
                        image_url="/static/pll/J1.webp",
                    ),
                    Algorithm(
                        name="J permutation : b",
                        moves=["R U R' F' R U R' U' R' F R2 U' R' U'"],
                        image_url="/static/pll/J.webp",
                    ),
                    Algorithm(
                        name="N permutation : a",
                        moves=[
                            "R U R' U R U R' F' R U R' U' R' F R2 U' R' U2 R U' R'",
                            "F' R U R' U' R' F R2 F U' R' U' R U F' R'",
                        ],
                        image_url="/static/pll/N1.webp",
                    ),
                    Algorithm(
                        name="N permutation : b",
                        moves=["(R' U R U' R') (F' U' F) (R U R') (F R' F') (R U' R)"],
                        image_url="/static/pll/N.webp",
                    ),
                    Algorithm(
                        name="R permutation : a",
                        moves=[
                            "(y') R U' R' U' R U R D R' U' R D' R' U2 R'",
                            "(y') R U R' F' R U2 R' U2 R' F R U R U2 R'",
                        ],
                        image_url="/static/pll/R1.webp",
                    ),
                    Algorithm(
                        name="R permutation : b",
                        moves=[
                            "R' U2 R U2 R' F (R U R' U') R' F' R2' U'",
                            "R' U2 R' D' R U' R' D R U R U' R' U' R",
                        ],
                        image_url="/static/pll/R.webp",
                    ),
                    Algorithm(
                        name="T permutation",
                        moves=[
                            "R U R' F' R U R' U' R' F R2 U' R'",
                            "R U R' U' R' F R2 U' R' U F' L' U L",
                        ],
                        image_url="/static/pll/T.webp",
                    ),
                    Algorithm(
                        name="V permutation",
                        moves=[
                            "R' U R' U' R D' R' D R3 U D' R2 U' R2' D R2",
                            "R' U R' U' (y) R' F' R2 U' R' U R' F R F",
                        ],
                        image_url="/static/pll/V.webp",
                    ),
                    Algorithm(
                        name="Y permutation",
                        moves=["F R U' R' U' R U R' F' (R U R' U') (R' F R F')"],
                        image_url="/static/pll/Y.webp",
                    ),
                ],
            ),
        ],
    ),
)
