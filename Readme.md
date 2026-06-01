# create_datasets

Tools for creating multimodal datasets from CQPWeb search results.

This repository contains the dataset-creation pipeline used to extract short video clips around queried linguistic expressions, filter candidate clips, process them with OpenPose, and organize the resulting data for multimodal analysis of speech and gesture.

The pipeline was developed for research on the relation between linguistic expressions and co-speech gesture. It is especially useful when researchers need multiple video tokens of the same word, phrase, or construction across many speakers.

The examples below use the temporal deictic expressions yesterday, today, and tomorrow, which correspond to the type of dataset discussed in the associated article.

For questions about this repository or the dataset-creation workflow, please contact:

Raúl Sánchez  
raul@um.es

---

# Overview of the pipeline

Starting from a CQPWeb tabulation exported from NewsScape/Labyrinth, the pipeline:

1. searches for a linguistic expression in CQPWeb;
2. downloads the CQPWeb tabulation containing the timing of each hit;
3. extracts short video clips around each occurrence of the expression;
4. organizes the resulting clips into a dataset folder;
5. checks whether a visible person is present in the clip;
6. filters clips where the relevant speaker or upper-body keypoints are not reliably detected;
7. stores the accepted videos and metadata;
8. prepares the dataset for downstream multimodal analysis.

The resulting dataset can then be processed with OpenPose and with R tools such as dfmaker, xycorrector, and cramerOpenPose to convert raw image coordinates into body-centered normalized coordinates.

---

# 1. Download links to clips from CQPWeb

We are going to create a dataset of clips containing temporal expressions such as:

- yesterday
- today
- tomorrow

First, go to CQPWeb and search for the target expression (https://corpus.multi-data.eu).

For example:

![cqpweb1](https://github.com/user-attachments/assets/10ac21a1-115a-40da-ac26-8386f10fd5cd)

Click on tabulate.

![cqpweb2](https://github.com/user-attachments/assets/c7759f07-8da6-4802-81c6-096cac7b585b)


On the next page:

1. Click on Create bigger form.
2. Fill the attribute fields as follows:

```text text_file       Structure text_file text_id         Structure text_id startsecs startcentisecs endsecs endcentisecs ```

3. Click on Download query tabulation with settings above.

![cqpweb3](https://github.com/user-attachments/assets/fb8824bb-34d5-42b1-ae3c-e885f5232453)

You will get a tabulation file with rows like this:

<code>
csv 2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    204    61    204    79 2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    296    83    296    343 2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    1199    539    1199    799 2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    1392    211    1392    471 2017-07-21_1000_US_MSNBC_Morning_Joe.txt    t__5c626584_6dfb_11e7_8c64_089e01ba0326    1814    779    1815    259 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    13    518    13    858 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    109    914    110    154 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    733    51    733    79 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    960    7    961    81 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    1747    206    1747    667 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2130    57    2130    397 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2131    918    2132    178 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2232    11    2232    292 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2427    799    2428    2 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    2883    32    2883    172 2017-07-21_1800_US_CNN_CNN_Newsroom_With_Brooke_Baldwin.txt    t__6a7fc45c_6e3e_11e7_80e2_2c600c9500f4    3066    347    3066    668 2017-07-21_0000_US_KABC_Eyewitness_News_5PM.txt    t__8b4e67c0_6da7_11e7_a46a_089e01ba0335    359    5    359    31 
</code>

The expected fields are:

```text text_file text_id startsecs startcentisecs endsecs endcentisecs```

These timing fields are used to locate the target expression and extract a video window around it.

For clarity, save the tabulation files with informative names, for example:

```tmp/tabulation_yesterday.txt tmp/tabulation_today.txt tmp/tabulation_tomorrow.txt ```

---

# 2. Install create_datasets tools

Terminal knowledge is required from this point.

First, create the environment and install the dependencies:

```bash conda create -n pipeline_datasets python=3.12 -y conda activate pipeline_datasets pip install -r requirements.txt ```

External requirements include:

- ffmpeg, for video clipping;
- OpenPose, for body keypoint detection;
- access to the relevant NewsScape/Labyrinth video files;
- R, for downstream dataset processing and coordinate normalization.

---

# 3. Basic usage

The following examples create datasets for yesterday, today, and tomorrow.

## Example: yesterday

```bash ./create_dataset.py \   --input tmp/tabulation_yesterday.txt \   --output_folder tmp/yesterday \   --searchterm yesterday \   --offset 2 ```

You will get the dataset in: ```tmp/yesterday/dataset.duckdb```

The accepted videos will be stored in: ```tmp/yesterday/videos/good```

## Example: today

```bash ./create_dataset.py \   --input tmp/tabulation_today.txt \   --output_folder tmp/today \   --searchterm today \   --offset 2 ```

You will get the dataset in: ```tmp/today/dataset.duckdb```

The accepted videos will be stored in: ```tmp/today/videos/good```

## Example: tomorrow

```bash ./create_dataset.py \   --input tmp/tabulation_tomorrow.txt \   --output_folder tmp/tomorrow \   --searchterm tomorrow \   --offset 2 ```

You will get the dataset in: ```tmp/tomorrow/dataset.duckdb```

The accepted videos will be stored in: ```tmp/tomorrow/videos/good```

The --offset parameter controls the temporal window around the target expression. For example, --offset 2 extracts approximately two seconds before and two seconds after the queried expression.

---

# 4. Main parameters

| Parameter | Description |
|---|---|
| --input | Path to the CQPWeb tabulation file |
| --output_folder | Folder where the dataset will be created |
| --searchterm | Target word or phrase used in the CQPWeb query |
| --offset | Number of seconds added before and after the target expression |

---

# 5. Repository structure

<code>
create_datasets/ ├── create_dataset.py                  # Main script for creating a dataset from CQPWeb tabulations 
                 ├── download_clips.py                  # Utilities for downloading/extracting clips 
                 ├── is_there_a_person_in_the_video.py  # OpenPose-based visible-person filtering
                 ├── prepare_words.R                    # Preparation of target expression lists 
                 ├── max_people_classification.R        # Auxiliary R script for person-count classification 
                 ├── requirements.txt                   # Python dependencies 
                 ├── exec.sh                            # Example shell execution 
                 └── speech_analysis/                   # Additional scripts for speech-related processing 
</code>

---

# 6. Output

A successful run produces a folder such as:

<code>
tmp/yesterday/ 
              ├── dataset.duckdb 
              ├── videos/ │   
              ├── good/ │   
              ├── rejected/ 
          │   └── ... └── metadata/ 
</code>

The exact folder structure may vary depending on the configuration and processing stage.

---

# 7. Filtering and quality control

The pipeline includes automatic and manual filtering steps.

Automatic filtering removes clips where no visible person or no relevant upper-body keypoints are detected. This is done using OpenPose-based checks.

Manual filtering is still necessary because some clips may contain:

- voice-over speech;
- camera cuts during the target expression;
- repeated commercials or repeated broadcast segments;
- visible people who are not the active speaker;
- unclear shots or partial bodies;
- multiple speakers requiring human disambiguation.

For the study associated with this repository, the final dataset was manually checked to ensure that the visible speaker was the person uttering the target expression.

---

# 8. OpenPose and coordinate processing

OpenPose provides frame-level 2D body keypoints in image coordinates. These raw coordinates depend on camera position, video resolution, body size, and the speaker’s position in the frame.

For downstream analysis, the coordinates should be transformed into a body-centered coordinate system. In the associated study, this was done with the R functions:

- dfmaker
- xycorrector
- cramerOpenPose

These functions convert OpenPose JSON files into structured data and normalize coordinates relative to the speaker’s body. The chest keypoint is used as the origin, the shoulder line defines the horizontal axis, and distances are scaled by the chest-to-shoulder span. This makes coordinates comparable across speakers and videos.

---

# 9. Notes on smoothing

The analyses reported in the associated article did not apply additional smoothing to the OpenPose wrist coordinates. The pilot analysis used frame-level OpenPose detections after body-centered coordinate normalization.

Smoothing and trajectory reconstruction are planned for later analyses focused on time-resolved gesture dynamics.

---

# 10. Relation to the associated paper

This repository supports the dataset-building workflow described in:

“Studying the gesture-speech relation through novel multimodal datasets”

The repository documents the executable part of the pipeline used to move from CQPWeb/NewsScape search results to an analysable multimodal dataset.

A fuller methodological description of the corpus-creation procedure is being prepared separately as:

Sánchez et al. (in preparation)

The associated article focuses on the linguistic and statistical potential of the resulting dataset, while this repository provides the practical basis for reproducing and extending the dataset-building workflow.

---

# 11. Citation

If you use this repository, please cite the associated article and the relevant tools used in the pipeline, including NewsScape, CQPWeb, OpenPose, and multimolang.In preparation

---

# 12. Status

This repository is under active development. Interfaces, file structure, and script names may change as the pipeline is consolidated and documented.
