# Musician_Plan

music analyzer的小项目，最终想知道怎么理解音乐的结构还有带给人的情感，以及如果要成为视频背景音乐的话，如何更好找到切分点。初步想法是能够拆分音乐的元素，目前做了基础beat的，实时tempo，不同频段的peak，音调chroma.


## Requirements

```{bash}
pip install -r requirements.txt
```

## How to Play

```{python}
python beat-detect.py {Relative Path to the WAV file} # python beat-detect.py "music/One Last Kiss.wav"
```

## Demo

https://github.com/mathildasy/Musician_Plan/blob/main/demo.mp4
