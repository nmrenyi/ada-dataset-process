# ada-dataset-process
processing YouNiverse dataset for ADAcadabra2048 project

## File descriptions

According to Bich Ngoc Doan's requirements, I sorted the video metadata `yt_metadata_en.jsonl` descendingly by the dislike_count and dislike_count / (like_count + dislike_count), respectively, resulting in `yt_metadata_en_sorted_abs.jsonl` and `yt_metadata_en_sorted_rel.jsonl` (`abs` and `rel` in file name, representing if the file is sorted by absolute value of dislike_count or the relative value of dislike_count, as is defind above). These two files are 97.62GB and 99.93GB, respectively, stored only on my portable SSD.

To make it easier to process these two large files, I only extracted some columns including the basic information from `yt_metadata_en_sorted_abs.jsonl` and `yt_metadata_en_sorted_rel.jsonl`, resulting in `yt_metadata_en_sorted_abs_basic.csv` and `yt_metadata_en_sorted_rel_basic.csv` (sepearted by \t, not comma). The included columns are: 
```bash
categories      upload_date     crawl_date      like_count      dislike_count   view_count      display_id      channel_id
```
where the `upload_date` and `crawl_date` only includes the year, without the month, day and time, for space efficiency.

Both `yt_metadata_en_sorted_abs_basic.csv` and `yt_metadata_en_sorted_rel_basic.csv` have size 5.54GB. I compressed them seperately into `yt_metadata_en_sorted_abs_basic.csv.zip` and `yt_metadata_en_sorted_rel_basic.csv.zip`, with size 1.4GB and 1.77GB, respectively. You can find these two files on our shared Google Drive with path `ADAcadabra/dataset`.

From `yt_metadata_en_sorted_abs_basic.csv` and `yt_metadata_en_sorted_rel_basic.csv`, as Bich Ngoc Doan required, I further filtered out data with specific category and upload year. There are 17 categories and 15 years, resulting in 17 * 15 = 255 files, for each sorting method (sorted by absolute or relative dislike count). 

For example `Autos & Vehicles_2005.csv` in `specified_category_year_abs` folder means that it's the file with category `Autos & Vehicles` and year `2005`, sorted by absolute dislike count (#dislike). `Gaming_2010.csv` in `specified_category_year_rel` folder means that it's the file with category `Gaming` and year `2010`, sorted by relative dislike count (#dislike / (#like + #dislike)). Caution: these files could be empty, e.g. `specified_category_year_rel/Movies_2005.csv`, indicating that there's no video in Movies category in 2005 in our dataset file `yt_metadata_en.jsonl`.

I compressed these files into `specified_category_year_abs.zip` and `specified_category_year_rel.zip`, with size 1.35GB and 1.64GB. You can find these two files on our shared Google Drive with path `ADAcadabra/dataset`.

Please contact Ren Yi at yi.ren@epfl.ch for further questions.
