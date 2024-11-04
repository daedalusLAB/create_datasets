# Download links to clips

We are going to create a “test” dataset of clips containing the expression: **before**

First of all, we’ll go to Labyrinth’s CQPweb and search for the term:

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/1fe82bf0-ea44-4964-8530-15f05c1f2ffd/7e8b6599-a6c9-4227-adb9-9696dcc5112b/image.png)

Click on “**tabulate**”

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/1fe82bf0-ea44-4964-8530-15f05c1f2ffd/0adebf12-7dd4-49ca-a342-764792e65626/image.png)

In next page you have to:

 

1. Click on “Create bigger form”
2. Fill the attribute fields as this:
    
    • text_file (Structure text_file)
    • text_id (Structure text_id)
    • startsecs
    • startcentisecs
    • endsecs
    • endcentisecs
    
3. Click on “Download query tabulation with settings above”

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/1fe82bf0-ea44-4964-8530-15f05c1f2ffd/434f508c-5339-4ebe-b6f0-7661a951001d/image.png)

You get a file like this: 

[tabulation_before_100.txt](https://prod-files-secure.s3.us-west-2.amazonaws.com/1fe82bf0-ea44-4964-8530-15f05c1f2ffd/3aefd5b5-42a6-4bac-bf4c-a799707f5cc2/tabulation_before_100.txt)

```python
2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    204    61    204    79
2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    296    83    296    343
2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    1199    539    1199    799
2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    1392    211    1392    471
2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    1814    779    1815    259
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    13    518    13    858
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    109    914    110    154
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    733    51    733    79
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    960    7    961    81
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    1747    206    1747    667
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2130    57    2130    397
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2131    918    2132    178
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2232    11    2232    292
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2427    799    2428    2
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2883    32    2883    172
2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    3066    347    3066    668
2017-07-21_0000_US_KABC_Eyewitness_News_5PM.txt    t__8b4e67c0_6da7_11e7_a46a_089e01ba0335    359    5    359    31
```

# Install create_datasets tools

**Terminal knowledge is required from now on.**

First, create the environment and install dependences:

```python
 conda create -n pipeline_datasets python=3.12 -y
 conda activate pipeline_datasets
 pip install -r requirements.txt
```

And use this way

```python
./create_dataset.py --input tmp/tabulation_before_100.txt \
        --output_folder tmp/before_100 \
        --searchterm before \ 
        --offset 2
```

You will get the dataset in tmp/before_100/dataset.duckdb and videos used in tmp/before_100/videos/good
