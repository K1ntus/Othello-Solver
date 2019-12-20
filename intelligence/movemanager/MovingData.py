'''
Created on 18 déc. 2019

Script that contains a list of Opening Move following our
hashing method. These moves can be found on internet and has 
been converted to make them compatible with our reversi
board version. (Usually, Board is 8x8 while it is 
currently 10x10. Which is changing the position of every 
tokens.'''



    
        

__moveList__ = [
    "d4D5",  #@Diagonal Opening
    "C3d4E4D5d6",  #@X-square Opening (t3)
    "d4E4C4D5d6",  #@Snake", Peasant (t3)
    "d4E4C4D5g5c5d6C6G6D7e7",  #@Pyramid", Checkerboarding Peasant (t3)
    "d4E4D5C5d6",  #@Heath", Tobidashi "Jumping Out" (t3)
    "e3D3d4E4D5C5g5d6G6E7d7f7G8",  #@Mimura variation II** (t3)
    "e3d4E4D5C5d6E7",  #@Heath-Bat (t3)
    "e3F3d4E4D5C5d6",  #@Iwasaki variation** (t3)
    "d4E4f4D5C5d6",  #@Heath-Chimney", "Mass-Turning" (t3)
    "d4E4D5d6C6",  #@Raccoon Dog (t3)
    "d4E4D5d6C6C7d7",  #@Hamilton (t3)
    "d4E4f4D5d6C7",  #@Lollipop (t3)
    "d4E4D5d6E7",  #@Cow (t3)
    "d4E4f4D5d6E7",  #@Chimney (t3)
    "d4E4D5g5C5d6E7",  #@Cow Bat", Bat", Cambridge (t3)
    "d4E4C4D5g5C5d6C6E7c7d7",  #@Bat (Piau Continuation 2)** (t3)
    "d4E4D5g5C5d6C6G6E7c7d7",  #@Melnikov**", Bat (Piau Continuation 1)** (t3)
    "D3E3d4E4c4f4D5g5C5b5d6C6B6E7d7C7b7",  #@Bat (Kling Continuation)** (t3)
    "d4E4f4C4D5g5C5d6E7",  #@Bat (Kling Alternative)** (t3)
    "d4E4D5g5d6G6E7",  #@Rose-v-Toth** (t3)
    "e3d4E4D5g5d6G6E7",  #@Tanida (t3)
    "e3d4E4D5g5d6G6C6E7",  #@Aircraft", Feldborg (t3)
    "e3d4E4D5g5H5d6G6E7e8",  #@Sailboat (t3)
    "d4E4D5g5d6G6E7f7D7e8",  #@Maruoka (t3)
    "d4E4D5g5d6G6E7f7G7",  #@Landau (t3)
    "d4E4D5d6G7",  #@Buffalo", Kenichi Variation (t3)
    "f3d4E4D5d6G7D7",  #@Maruoka Buffalo** (t3)
    "d4E4f4D5G5d6g6h6G7D7",  #@Tanida Buffalo (t3)
    "d4E4D5d6g6G7",  #@Hokuriku Buffalo (t3)
    "C3d4E4f4D5",  #@X-square Opening (t3)
    "D3d4E4f4D5",  #@Snake", Peasant (t3)
    "D3F3e3d4E4f4G4D5g5e7F7",  #@Pyramid", Checkerboarding Peasant (t3)
    "E3d4E4f4D5",  #@Heath", Tobidashi "Jumping Out" (t3)
    "E3d4E4f4C4g4D5c5G5g6e7F7H7",  #@Mimura variation II** (t3)
    "E3d4E4f4D5c5C6",  #@Iwasaki variation** (t3)
    "E3d4E4f4D5c5G5",  #@Heath-Bat (t3)
    "E3d4E4f4D5d6",  #@Heath-Chimney", "Mass-Turning" (t3)
    "F3d4E4f4D5",  #@Raccoon Dog (t3)
    "G3d4E4f4D5d6",  #@Lollipop (t3)
    "G3F3d4E4f4g4D5",  #@Hamilton (t3)
    "d4E4f4D5G5",  #@Cow (t3)
    "d4E4f4D5G5d6",  #@Chimney (t3)
    "E3d4E4f4D5G5e7",  #@Cow Bat", Bat", Cambridge (t3)
    "E3D3d4E4f4D5G5d6e7",  #@Bat (Kling Alternative)** (t3)
    "E3g3F3D3d4E4f4g4D5G5e7",  #@Bat (Piau Continuation 2)** (t3)
    "E3g3F3d4E4f4g4D5G5e7F7",  #@Melnikov**", Bat (Piau Continuation 1)** (t3)
    "e2F2g2E3F3d3G3d4E4f4g4C4D5G5C5d6e7",  #@Bat (Kling Continuation)** (t3)
    "d4E4f4D5G5e7F7",  #@Rose-v-Toth** (t3)
    "d4E4f4D5G5c5e7F7",  #@Tanida (t3)
    "d4E4f4D5G5c5h5e7F7E8",  #@Sailboat (t3)
    "F3d4E4f4D5G5c5e7F7",  #@Aircraft", Feldborg (t3)
    "d4E4f4G4D5G5h5g6e7F7",  #@Maruoka (t3)
    "d4E4f4D5G5g6e7F7G7",  #@Landau (t3)
    "d4E4f4D5G7",  #@Buffalo", Kenichi Variation (t3)
    "d4E4f4G4D5c6G7",  #@Maruoka Buffalo** (t3)
    "d4E4f4G4D5d6G7f7E7f8",  #@Tanida Buffalo (t3)
    "d4E4f4D5G7f7",  #@Hokuriku Buffalo (t3)
    "d4D5d6F7",  #@Wing Variation
    "d4D5G6d6",  #@Semi-Wing Variation@@@
    "D5d6",  #@Parallel Opening
    "f4D5",  #@Perpendicular Opening
    "f4D5G5d6E7f7",  #@Mimura
    "f4g4D5G5d6E7D7",  #@Shaman", Danish
    "f4g4E4D5G5d6E7",  #@Inoue
    "f4g4E4d4D5G5d6E7",  #@IAGO
    "F3f4g4D5G5d6E7",  #@Bhagat
    "f3f4g4d4E4D5G5d6E7F7",  #@Rose
    "f3f4g4d4E4D5G5d6C6E7F7",  #@Flat
    "f3f4g4d4E4D5G5d6C6g6E7F7",  #@Rotating Flat
    "f3f4g4d4E4C4D5G5d6C6g6E7F7",  #@Murakami Variation**
    "f3D3E3f4g4d4E4D5G5C5d6C6g6E7F7g7f8d8",  #@Rotating Flat** (Kling Continuation)
    "f3f4g4d4E4D5G5d6g6E7F7C7",  #@Rose-Birth**
    "f3f4g4d4E4D5G5C5d6g6H6E7F7C7g7e8",  #@Brightstein
    "f3f4g4d4E4D5G5d6g6H6E7F7C7",  #@Rose-birdie", Rose-Tamenori
    "f3f4g4d4E4D5G5d6g6H6E7F7C7g7",  #@Rose-Tamenori-Kling**
    "f3E3f4g4d4E4D5G5d6E7F7",  #@Greenberg", Dawg
    "f4g4D5G5d6E7F7d7",  #@Ralle
    "f4D5G5d6F7",  #@Horse
    "f4D5c5G6",  #@No-Cat**
    "f4G4D5c5G6",  #@Swallow
    "F3f4G4D5c5g5G6H6f7g7E7d7",  #@No-Cat** (Continuation)
    "f4E4D5G6f7",  #@Italian
    "f4D5G5G6f7",  #@Cat
    "f4g4D5G5G6d6f7E7d7G8",  #@Sakaguchi**
    "f4D5G5G6d6h6f7E7d7H7G8",  #@Berner**
    "f4D5c5G7",  #@Ganglion
    "f4D5G6G7f7",  #@Tiger
    "f4D4D5G6d6G7f7",  #@Stephenson
    "f4D4D5c5G6d6G7f7",  #@No-Kung
    "f4D4D5c5G6d6C6G7f7E7d7b7C7d8",  #@No-Kung** (Continuation)
    "f4D4D5G6d6G7f7d7",  #@COMP'OTH
    "f4D4D5G6d6h6G7f7",  #@Kung
    "f4E4D5G6d6G7f7",  #@Leader's Tiger
    "f4D5G6d6G7f7E7",  #@Brightwell
    "f4g4e4D5G5H5G6d6h6G7f7D7E7",  #@Ishii**
    "F3f4g4e4c4D4D5G5H5c5G6d6h6G7f7D7E7c7",  #@Mainline Tiger**
    "f4D5G5G6d6G7f7h7G8",  #@Rose-BILL
    "f4e4D5G5G6d6G7f7h7G8",  #@Tamenori**
    "f4D5G6G7f7h7",  #@Aubrey", Tanaka
    "E4d4",  #@Diagonal Opening
    "C3E4d4D5d6",  #@X-square Opening (t3)
    "E4d4C4D5d6",  #@Snake", Peasant (t3)
    "E4d4C4D5g5c5d6C6G6D7e7",  #@Pyramid", Checkerboarding Peasant (t3)
    "E4d4D5C5d6",  #@Heath", Tobidashi "Jumping Out" (t3)
    "e3D3E4d4D5C5g5d6G6E7d7f7G8",  #@Mimura variation II** (t3)
    "e3E4d4D5C5d6E7",  #@Heath-Bat (t3)
    "e3F3E4d4D5C5d6",  #@Iwasaki variation** (t3)
    "E4d4f4D5C5d6",  #@Heath-Chimney", "Mass-Turning" (t3)
    "E4d4D5d6C6",  #@Raccoon Dog (t3)
    "E4d4D5d6C6C7d7",  #@Hamilton (t3)
    "E4d4f4D5d6C7",  #@Lollipop (t3)
    "E4d4D5d6E7",  #@Cow (t3)
    "E4d4f4D5d6E7",  #@Chimney (t3)
    "E4d4D5g5C5d6E7",  #@Cow Bat", Bat", Cambridge (t3)
    "E4d4C4D5g5C5d6C6E7c7d7",  #@Bat (Piau Continuation 2)** (t3)
    "E4d4D5g5C5d6C6G6E7c7d7",  #@Melnikov**", Bat (Piau Continuation 1)** (t3)
    "D3E3E4d4c4f4D5g5C5b5d6C6B6E7d7C7b7",  #@Bat (Kling Continuation)** (t3)
    "E4d4f4C4D5g5C5d6E7",  #@Bat (Kling Alternative)** (t3)
    "E4d4D5g5d6G6E7",  #@Rose-v-Toth** (t3)
    "e3E4d4D5g5d6G6E7",  #@Tanida (t3)
    "e3E4d4D5g5d6G6C6E7",  #@Aircraft", Feldborg (t3)
    "e3E4d4D5g5H5d6G6E7e8",  #@Sailboat (t3)
    "E4d4D5g5d6G6E7f7D7e8",  #@Maruoka (t3)
    "E4d4D5g5d6G6E7f7G7",  #@Landau (t3)
    "E4d4D5d6G7",  #@Buffalo", Kenichi Variation (t3)
    "f3E4d4D5d6G7D7",  #@Maruoka Buffalo** (t3)
    "E4d4f4D5G5d6g6h6G7D7",  #@Tanida Buffalo (t3)
    "E4d4D5d6g6G7",  #@Hokuriku Buffalo (t3)
    "C3E4d4f4D5",  #@X-square Opening (t3)
    "D3E4d4f4D5",  #@Snake", Peasant (t3)
    "D3F3e3E4d4f4G4D5g5e7F7",  #@Pyramid", Checkerboarding Peasant (t3)
    "E3E4d4f4D5",  #@Heath", Tobidashi "Jumping Out" (t3)
    "E3E4d4f4C4g4D5c5G5g6e7F7H7",  #@Mimura variation II** (t3)
    "E3E4d4f4D5c5C6",  #@Iwasaki variation** (t3)
    "E3E4d4f4D5c5G5",  #@Heath-Bat (t3)
    "E3E4d4f4D5d6",  #@Heath-Chimney", "Mass-Turning" (t3)
    "F3E4d4f4D5",  #@Raccoon Dog (t3)
    "G3E4d4f4D5d6",  #@Lollipop (t3)
    "G3F3E4d4f4g4D5",  #@Hamilton (t3)
    "E4d4f4D5G5",  #@Cow (t3)
    "E4d4f4D5G5d6",  #@Chimney (t3)
    "E3E4d4f4D5G5e7",  #@Cow Bat", Bat", Cambridge (t3)
    "E3D3E4d4f4D5G5d6e7",  #@Bat (Kling Alternative)** (t3)
    "E3g3F3D3E4d4f4g4D5G5e7",  #@Bat (Piau Continuation 2)** (t3)
    "E3g3F3E4d4f4g4D5G5e7F7",  #@Melnikov**", Bat (Piau Continuation 1)** (t3)
    "e2F2g2E3F3d3G3E4d4f4g4C4D5G5C5d6e7",  #@Bat (Kling Continuation)** (t3)
    "E4d4f4D5G5e7F7",  #@Rose-v-Toth** (t3)
    "E4d4f4D5G5c5e7F7",  #@Tanida (t3)
    "E4d4f4D5G5c5h5e7F7E8",  #@Sailboat (t3)
    "F3E4d4f4D5G5c5e7F7",  #@Aircraft", Feldborg (t3)
    "E4d4f4G4D5G5h5g6e7F7",  #@Maruoka (t3)
    "E4d4f4D5G5g6e7F7G7",  #@Landau (t3)
    "E4d4f4D5G7",  #@Buffalo", Kenichi Variation (t3)
    "E4d4f4G4D5c6G7",  #@Maruoka Buffalo** (t3)
    "E4d4f4G4D5d6G7f7E7f8",  #@Tanida Buffalo (t3)
    "E4d4f4D5G7f7",  #@Hokuriku Buffalo (t3)
    "E4d4f4F7",  #@Semi-Wing Variation
    "E4d4f4G6",  #@Wing Variation
    "E4d6",  #@Perpendicular Opening
    "E4f4G5d6C6E7d7",  #@Bhagat
    "E4f4G5D5d6E7d7",  #@Inoue
    "E4f4d4G5D5d6E7d7",  #@IAGO
    "E4f4G4G5d6E7d7",  #@Shaman", Danish
    "E4f4d4G5D5d6G6c6E7d7",  #@Rose
    "E4f4d4G5D5C5d6G6c6E7d7",  #@Greenberg", Dawg
    "F3E4f4d4G5D5d6G6c6E7d7",  #@Flat
    "F3E4f4d4G5D5d6G6c6E7d7f7",  #@Rotating Flat
    "F3D3E4f4d4G5D5d6G6c6E7d7f7",  #@Murakami Variation**
    "F3E3E4f4d4C4h4G5D5C5d6G6c6h6E7d7f7g7",  #@Rotating Flat** (Kling Continuation)
    "G3E4f4d4G5D5d6G6c6E7d7f7",  #@Rose-Birth**
    "G3E3E4f4d4G5D5h5d6G6c6E7d7f7g7F8",  #@Brightstein
    "G3E4f4d4G5D5d6G6c6E7d7f7F8",  #@Rose-birdie", Rose-Tamenori
    "G3E4f4d4G5D5d6G6c6E7d7f7g7F8",  #@Rose-Tamenori-Kling**
    "E4f4g4G5d6G6E7d7",  #@Ralle
    "E4f4G5d6g6E7",  #@Mimura
    "E4f4d6G6E7",  #@Horse
    "e3E4d6F7",  #@No-Cat**
    "e3E4d6F7D7",  #@Swallow
    "e3E4g4G5d6C6g6F7D7e7g7F8",  #@No-Cat** (Continuation)
    "E4D5d6g6F7",  #@Italian
    "E4d6g6F7E7",  #@Cat
    "E4f4g4G5d6g6F7E7H7d7",  #@Sakaguchi**
    "E4f4g4G5d6g6F7E7H7f8G8",  #@Berner**
    "e3E4d6G7",  #@Ganglion
    "E4d6g6G7F7",  #@Tiger
    "E4f4D4d6g6G7F7",  #@Stephenson
    "e3E4f4D4d6g6G7F7",  #@No-Kung
    "g2e3F3G3E4f4D4g4h4G5d6g6G7F7",  #@No-Kung** (Continuation)
    "E4f4D4d6g6G7F7f8",  #@Kung
    "E4f4D4g4d6g6G7F7",  #@COMP'OTH
    "E4f4D5d6g6G7F7",  #@Leader's Tiger
    "E4f4G4d5G5d6g6G7F7E7d7f8E8",  #@Ishii**
    "d3e3g3E4f4G4D4d5G5d6g6C6G7F7E7d7f8E8",  #@Mainline Tiger**
    "E4f4d6g6G7F7E7H7g8",  #@Rose-BILL
    "E4f4d5d6g6G7F7E7H7g8",  #@Tamenori**
    "E4f4G5d6g6G7F7",  #@Brightwell
    "E4d6g6G7F7g8",  #@Aubrey", Tanaka
    "E4f4",  #@Parallel Opening @@@
    "F7e7",  #@Parallel Opening
    "g5F7",  #@Perpendicular Opening
    "D4E4g5d5F7",  #@Tiger
    "d3D4E4g5d5F7",  #@Aubrey", Tanaka
    "D4E4g5d5D6F7e7",  #@Brightwell
    "d3D4E4F4C4g5d5F7e7",  #@Rose-BILL
    "d3D4E4F4C4g5d5g6F7e7",  #@Tamenori**
    "e3F3D4E4F4g4g5d5g6D6F7e7D7",  #@Ishii**
    "e3F3D4E4F4g4g5d5H5g6D6F7e7D7G7g8f8d8",  #@Mainline Tiger**
    "D4E4g5d5G6F7e7",  #@Leader's Tiger
    "D4E4g5d5F7e7G7",  #@Stephenson
    "D4E4g5d5F7e7G7d7",  #@COMP'OTH
    "e3D4E4g5d5F7e7G7",  #@Kung
    "D4E4g5d5F7e7G7f8",  #@No-Kung
    "D4E4g5d5D6F7e7G7d7c7f8E8D8d9",  #@No-Kung** (Continuation)
    "D4g5F7f8",  #@Ganglion
    "E4F4g5d5F7",  #@Cat
    "e3D3E4F4C4g5d5D6F7e7d7",  #@Berner**
    "E4F4C4g4g5d5D6F7e7d7",  #@Sakaguchi**
    "E4g5d5G6F7",  #@Italian
    "E4g5F7f8",  #@No-Cat**
    "E4G4g5F7f8",  #@Swallow
    "E3E4G4f4d4g5H5d5D6F7d7f8",  #@No-Cat** (Continuation)
    "F4g5D5F7e7",  #@Horse
    "F4g5d5D6F7e7",  #@Mimura
    "F4g4g5D5D6F7e7d7",  #@Ralle
    "F4g4g5D5h5D6G6F7e7g7",  #@Rose
    "F4g4e4g5D5h5D6G6F7e7g7D8",  #@Rose-Birth**
    "E3F4g4e4g5D5h5D6G6F7e7g7D8",  #@Rose-birdie", Rose-Tamenori
    "E3F4g4e4d4g5D5h5D6G6F7e7g7D8",  #@Rose-Tamenori-Kling**
    "E3F4g4e4d4g5D5h5D6G6c6F7e7g7D8F8",  #@Brightstein
    "F4g4g5D5h5D6G6F7e7g7E8",  #@Flat
    "F4g4e4g5D5h5D6G6F7e7g7E8",  #@Rotating Flat
    "F4g4e4d4g5D5h5c5D6G6H6F7e7g7H7c7E8F8",  #@Rotating Flat** (Kling Continuation)
    "F4g4e4g5D5h5D6G6F7e7g7E8G8",  #@Murakami Variation**
    "F4g4g5D5h5D6G6H6F7e7g7",  #@Greenberg", Dawg
    "F4g4g5D6F7e7D7",  #@Shaman", Danish
    "F4g4g5D6G6F7e7",  #@Inoue
    "F4g4g5D6G6F7e7g7",  #@IAGO
    "F4g4g5H5D6F7e7",  #@Bhagat
    "F7g7",  #@Diagonal Opening
    "D5F7g7e7",  #@Wing Variation
    "E4F7g7e7",  #@Semi-Wing Variation
    "D4G6F7g7e7",  #@Buffalo", Kenichi Variation (t3)
    "D4e4G6F7g7e7",  #@Hokuriku Buffalo (t3)
    "e3D4e4F4g5G6F7g7e7D7",  #@Tanida Buffalo (t3)
    "D4h5G6F7g7e7D7",  #@Maruoka Buffalo** (t3)
    "G6D6F7g7e7",  #@Cow (t3)
    "f4E4G6D6F7g7e7",  #@Rose-v-Toth** (t3)
    "f4E4D4d5G6D6F7g7e7",  #@Landau (t3)
    "f4E4d5G6D6c6F7g7e7D7",  #@Maruoka (t3)
    "f4E4G6D6h6F7g7e7",  #@Tanida (t3)
    "f4E4G6D6h6F7g7e7E8",  #@Aircraft", Feldborg (t3)
    "F3f4E4G6D6h6c6F7g7e7",  #@Sailboat (t3)
    "f4G6D6F7g7e7F8",  #@Cow Bat", Bat", Cambridge (t3)
    "f4g5G6D6H6F7g7e7d7H7F8E8g8D8f9E9d9",  #@Bat (Kling Continuation)** (t3)
    "f4E4G6D6F7g7e7d7F8d8E8",  #@Melnikov**", Bat (Piau Continuation 1)** (t3)
    "f4G6D6F7g7e7d7F8d8E8G8",  #@Bat (Piau Continuation 2)** (t3)
    "f4g5G6D6F7g7e7F8G8",  #@Bat (Kling Alternative)** (t3)
    "g5G6D6F7g7e7",  #@Chimney (t3)
    "G6F7g7e7d7D8E8",  #@Hamilton (t3)
    "g5G6F7g7e7D8",  #@Lollipop (t3)
    "G6F7g7e7E8",  #@Raccoon Dog (t3)
    "G6F7g7e7F8",  #@Heath", Tobidashi "Jumping Out" (t3)
    "g5G6F7g7e7F8",  #@Heath-Chimney", "Mass-Turning" (t3)
    "G6h6D6F7g7e7F8",  #@Heath-Bat (t3)
    "H5G6h6F7g7e7F8",  #@Iwasaki variation** (t3)
    "f4E4C4d5G6h6D6F7g7e7H7d7F8",  #@Mimura variation II** (t3)
    "G6F7g7e7G8",  #@Snake", Peasant (t3)
    "f4E4G6d6F7g7e7D7G8E8f8",  #@Pyramid", Checkerboarding Peasant (t3)
    "G6F7g7e7H8",  #@X-square Opening (t3)
    "D4g5G6F7g7",  #@Buffalo", Kenichi Variation (t3)
    "D4g5d5G6F7g7",  #@Hokuriku Buffalo (t3)
    "D4G4g5d5c5G6D6F7g7e7",  #@Tanida Buffalo (t3)
    "D4G4g5G6F7g7e8",  #@Maruoka Buffalo** (t3)
    "F4g5G6F7g7",  #@Cow (t3)
    "F4g5D5G6d6F7g7",  #@Rose-v-Toth** (t3)
    "F4e4D4g5D5G6d6F7g7",  #@Landau (t3)
    "f3F4e4G4g5D5G6d6F7g7",  #@Maruoka (t3)
    "F4g5D5G6d6F7g7f8",  #@Tanida (t3)
    "f3F4g5D5G6d6C6F7g7f8",  #@Sailboat (t3)
    "F4g5D5H5G6d6F7g7f8",  #@Aircraft", Feldborg (t3)
    "F4g5G6d6H6F7g7",  #@Cow Bat", Bat", Cambridge (t3)
    "F4g5G6d6H6F7g7e7H7",  #@Bat (Kling Alternative)** (t3)
    "F4g4H4i4g5H5I5G6d6H6i6F7g7h7e7G8F8",  #@Bat (Kling Continuation)** (t3)
    "F4h4g4g5H5D5G6d6H6F7g7",  #@Melnikov**", Bat (Piau Continuation 1)** (t3)
    "F4h4g4g5H5G6d6H6F7g7H7",  #@Bat (Piau Continuation 2)** (t3)
    "F4g5G6F7g7e7",  #@Chimney (t3)
    "H4g5G6F7g7e7",  #@Lollipop (t3)
    "H4g4g5H5G6F7g7",  #@Hamilton (t3)
    "g5H5G6F7g7",  #@Raccoon Dog (t3)
    "g5G6H6F7g7",  #@Heath", Tobidashi "Jumping Out" (t3)
    "g5G6H6F7g7e7",  #@Heath-Chimney", "Mass-Turning" (t3)
    "g5G6H6F7g7f8E8",  #@Iwasaki variation** (t3)
    "F4g5G6H6F7g7f8",  #@Heath-Bat (t3)
    "D3F4g4e4g5D5G6H6d6F7g7f8G8",  #@Mimura variation II** (t3)
    "g5G6F7g7H7",  #@Snake", Peasant (t3)
    "G4f4g5H5D5G6d6h6F7g7H7",  #@Pyramid", Checkerboarding Peasant (t3)
    "g5G6F7g7H8",  #@X-square Opening (t3)
    "G6e7",  #@Perpendicular Opening
    "D4e4D5G6e7",  #@Tiger
    "D4e4c4D5G6e7",  #@Aubrey", Tanaka
    "D3D4e4c4D5g5G6D6e7",  #@Rose-BILL
    "D3D4e4c4D5g5G6D6e7f7",  #@Tamenori**
    "D4e4G4F4D5g5c5G6D6C6e7d7f7",  #@Ishii**
    "D4e4G4F4h4D5g5c5G6D6C6h6e7d7f7h7G7E8",  #@Mainline Tiger**
    "D4e4F4D5g5G6e7",  #@Brightwell
    "D4e4D5g5G6e7F7",  #@Leader's Tiger
    "D4e4D5g5G6e7G7",  #@Stephenson
    "D4e4D5g5c5G6e7G7",  #@Kung
    "D4e4g4D5g5G6e7G7",  #@COMP'OTH
    "D4e4D5g5G6h6e7G7",  #@No-Kung
    "g3D4e4F4g4i4H4D5g5H5G6h6e7G7",  #@No-Kung** (Continuation)
    "D4G6h6e7",  #@Ganglion
    "e4D5G6D6e7",  #@Cat
    "D3e4F4g4C4D5g5c5G6D6e7",  #@Berner**
    "D3e4F4g4D5g5G6D6e7d7",  #@Sakaguchi**
    "e4D5G6e7F7",  #@Italian
    "D5G6h6e7",  #@No-Cat**
    "D5G6h6e7D7",  #@Swallow
    "e4d4F4g4D5C5G6h6d6e7D7E8",  #@No-Cat** (Continuation)
    "E4g5G6D6e7",  #@Horse
    "F4E4g4g5G6D6e7d7",  #@Ralle
    "F4E4g5G6D6e7d7g7F7e8",  #@Rose
    "F4E4g5G6D6e7d7g7F7e8F8",  #@Greenberg", Dawg
    "F4E4H4g5d5G6D6e7d7g7F7e8",  #@Rose-Birth**
    "F4E4H4g5d5C5G6D6e7d7g7F7e8",  #@Rose-birdie", Rose-Tamenori
    "F4E4H4d4g5d5C5G6D6e7d7g7F7e8",  #@Rose-Tamenori-Kling**
    "f3F4E4H4d4g5d5C5G6D6H6e7d7g7F7e8",  #@Brightstein
    "F4E4g5H5G6D6e7d7g7F7e8",  #@Flat
    "F4E4g5H5d5G6D6e7d7g7F7e8",  #@Rotating Flat
    "e3g3F4E4d4g5H5d5G6D6H6e7d7g7F7e8G8F8",  #@Rotating Flat** (Kling Continuation)
    "F4E4g5H5d5G6D6e7d7g7F7H7e8",  #@Murakami Variation**
    "F4g5G6D6e7d7E8",  #@Bhagat
    "F4g5G6D6e7d7F7",  #@Inoue
    "F4g5G6D6e7d7F7g7",  #@IAGO
    "F4G4g5G6D6e7d7",  #@Shaman", Danish
    "F4e4g5G6D6e7",  #@Mimura
    "g5G6",  #@Parallel Opening
    "G6g7",  #@Diagonal Opening
    "D5g5G6g7",  #@Semi-Wing Variation
    "E4g5G6g7",  #@Wing Variation
    "D4G6g7F7e7",  #@Buffalo", Kenichi Variation (t3)
    "D4e4G6g7F7e7",  #@Hokuriku Buffalo (t3)
    "e3D4e4F4g5G6g7F7e7D7",  #@Tanida Buffalo (t3)
    "D4h5G6g7F7e7D7",  #@Maruoka Buffalo** (t3)
    "G6D6g7F7e7",  #@Cow (t3)
    "f4E4G6D6g7F7e7",  #@Rose-v-Toth** (t3)
    "f4E4D4d5G6D6g7F7e7",  #@Landau (t3)
    "f4E4d5G6D6c6g7F7e7D7",  #@Maruoka (t3)
    "f4E4G6D6h6g7F7e7",  #@Tanida (t3)
    "f4E4G6D6h6g7F7e7E8",  #@Aircraft", Feldborg (t3)
    "F3f4E4G6D6h6c6g7F7e7",  #@Sailboat (t3)
    "f4G6D6g7F7e7F8",  #@Cow Bat", Bat", Cambridge (t3)
    "f4g5G6D6H6g7F7e7d7H7F8E8g8D8f9E9d9",  #@Bat (Kling Continuation)** (t3)
    "f4E4G6D6g7F7e7d7F8d8E8",  #@Melnikov**", Bat (Piau Continuation 1)** (t3)
    "f4G6D6g7F7e7d7F8d8E8G8",  #@Bat (Piau Continuation 2)** (t3)
    "f4g5G6D6g7F7e7F8G8",  #@Bat (Kling Alternative)** (t3)
    "g5G6D6g7F7e7",  #@Chimney (t3)
    "G6g7F7e7d7D8E8",  #@Hamilton (t3)
    "g5G6g7F7e7D8",  #@Lollipop (t3)
    "G6g7F7e7E8",  #@Raccoon Dog (t3)
    "G6g7F7e7F8",  #@Heath", Tobidashi "Jumping Out" (t3)
    "g5G6g7F7e7F8",  #@Heath-Chimney", "Mass-Turning" (t3)
    "G6h6D6g7F7e7F8",  #@Heath-Bat (t3)
    "H5G6h6g7F7e7F8",  #@Iwasaki variation** (t3)
    "f4E4C4d5G6h6D6g7F7e7H7d7F8",  #@Mimura variation II** (t3)
    "G6g7F7e7G8",  #@Snake", Peasant (t3)
    "f4E4G6d6g7F7e7D7G8E8f8",  #@Pyramid", Checkerboarding Peasant (t3)
    "G6g7F7e7H8",  #@X-square Opening (t3)
    "D4g5G6g7F7",  #@Buffalo", Kenichi Variation (t3)
    "D4g5d5G6g7F7",  #@Hokuriku Buffalo (t3)
    "D4G4g5d5c5G6D6g7F7e7",  #@Tanida Buffalo (t3)
    "D4G4g5G6g7F7e8",  #@Maruoka Buffalo** (t3)
    "F4g5G6g7F7",  #@Cow (t3)
    "F4g5D5G6d6g7F7",  #@Rose-v-Toth** (t3)
    "F4e4D4g5D5G6d6g7F7",  #@Landau (t3)
    "f3F4e4G4g5D5G6d6g7F7",  #@Maruoka (t3)
    "F4g5D5G6d6g7F7f8",  #@Tanida (t3)
    "f3F4g5D5G6d6C6g7F7f8",  #@Sailboat (t3)
    "F4g5D5H5G6d6g7F7f8",  #@Aircraft", Feldborg (t3)
    "F4g5G6d6H6g7F7",  #@Cow Bat", Bat", Cambridge (t3)
    "F4g5G6d6H6g7F7e7H7",  #@Bat (Kling Alternative)** (t3)
    "F4g4H4i4g5H5I5G6d6H6i6g7F7h7e7G8F8",  #@Bat (Kling Continuation)** (t3)
    "F4h4g4g5H5D5G6d6H6g7F7",  #@Melnikov**", Bat (Piau Continuation 1)** (t3)
    "F4h4g4g5H5G6d6H6g7F7H7",  #@Bat (Piau Continuation 2)** (t3)
    "F4g5G6g7F7e7",  #@Chimney (t3)
    "H4g5G6g7F7e7",  #@Lollipop (t3)
    "H4g4g5H5G6g7F7",  #@Hamilton (t3)
    "g5H5G6g7F7",  #@Raccoon Dog (t3)
    "g5G6H6g7F7",  #@Heath", Tobidashi "Jumping Out" (t3)
    "g5G6H6g7F7e7",  #@Heath-Chimney", "Mass-Turning" (t3)
    "g5G6H6g7F7f8E8",  #@Iwasaki variation** (t3)
    "F4g5G6H6g7F7f8",  #@Heath-Bat (t3)
    "D3F4g4e4g5D5G6H6d6g7F7f8G8",  #@Mimura variation II** (t3)
    "g5G6g7F7H7",  #@Snake", Peasant (t3)
    "G4f4g5H5D5G6d6h6g7F7H7",  #@Pyramid", Checkerboarding Peasant (t3)
    "g5G6g7F7H8",  #@X-square Opening (t3)
]



class OpeningMoveData:

    @staticmethod
    def getMoveList():
        return __moveList__


