python download_imageid_multi.py  -l demo.csv  -m_p  4  -th  0.4
sh gen_list.sh
wc -l demo.csv.imshow.lst
python remove_dup_images.py  demo.csv.imshow
sh gen_list.sh
wc -l demo.csv.imshow.lst

