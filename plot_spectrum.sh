# spectrum plotting using xpy
# @author: Leon Liang

# Generating a series of plots for each spectrum
# downloaded from WISeREP using xpy file from 
# the odetta group

# To allow permission, enter chmod u+x [.sh file]


# while IFS=$'\t' read -r data data_name
# do
# 	python ../../git/PCA/xpy --title "$data_name" -s 'all_supernovae/plots/spectra/'"$data_name" "$data"
# 	# echo "data is:" "$data"
# 	# echo "data_name is:" 'all_supernovae/plots/spectra/'"$data_name"

# done < <(paste 'all_supernovae/data.txt' 'all_supernovae/data_names.txt')

while IFS=$'\t' read -r data data_name
do
	python ../../git/PCA/xpy --title "$data_name" -s 'type_Ia/plots/spectra/'"$data_name" "$data"
	# echo "data is:" "$data"
	# echo "data_name is:" 'all_supernovae/plots/spectra/'"$data_name"

done < <(paste 'type_Ia/data.txt' 'type_Ia/data_names.txt')
echo "Done plotting type Ia with xpy" 

while IFS=$'\t' read -r data data_name
do
	python ../../git/PCA/xpy --title "$data_name" -s 'type_Ib/plots/spectra/'"$data_name" "$data"
	# echo "data is:" "$data"
	# echo "data_name is:" 'all_supernovae/plots/spectra/'"$data_name"

done < <(paste 'type_Ib/data.txt' 'type_Ib/data_names.txt')
echo "Done plotting type Ib with xpy" 

while IFS=$'\t' read -r data data_name
do
	python ../../git/PCA/xpy --title "$data_name" -s 'type_Ic/plots/spectra/'"$data_name" "$data"
	# echo "data is:" "$data"
	# echo "data_name is:" 'all_supernovae/plots/spectra/'"$data_name"

done < <(paste 'type_Ic/data.txt' 'type_Ic/data_names.txt')
echo "Done plotting type Ic with xpy" 

while IFS=$'\t' read -r data data_name
do
	python ../../git/PCA/xpy --title "$data_name" -s 'type_IIb/plots/spectra/'"$data_name" "$data"
	# echo "data is:" "$data"
	# echo "data_name is:" 'all_supernovae/plots/spectra/'"$data_name"

done < <(paste 'type_IIb/data.txt' 'type_IIb/data_names.txt')
echo "Done plotting type IIb with xpy" 

while IFS=$'\t' read -r data data_name
do
	python ../../git/PCA/xpy --title "$data_name" -s 'type_IIn/plots/spectra/'"$data_name" "$data"
	# echo "data is:" "$data"
	# echo "data_name is:" 'all_supernovae/plots/spectra/'"$data_name"

done < <(paste 'type_IIn/data.txt' 'type_IIn/data_names.txt')
echo "Done plotting type IIn with xpy" 

while IFS=$'\t' read -r data data_name
do
	python ../../git/PCA/xpy --title "$data_name" -s 'type_IIP/plots/spectra/'"$data_name" "$data"
	# echo "data is:" "$data"
	# echo "data_name is:" 'all_supernovae/plots/spectra/'"$data_name"

done < <(paste 'type_IIP/data.txt' 'type_IIP/data_names.txt')
echo "Done plotting type IIP with xpy" 

echo "Done plotting with xpy"
