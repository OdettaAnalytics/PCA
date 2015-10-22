mkdir type_all

ls -d type_* > types.txt

while IFS=$'\t' read -r type
do
	mkdir "$type"'/plots'
	mkdir "$type"'/plots/resolution'
	mkdir "$type"'/plots/spectra'
	mkdir "$type"'/plots/scale'
	mkdir "$type"'/plots/wavelength'

done < <(paste 'types.txt')

# mkdir 'all_supernovae'
# mkdir 'all_supernovae/plots'
# mkdir 'all_supernovae/plots/resolution'
# mkdir 'all_supernovae/plots/spectra'
# mkdir 'all_supernovae/plots/scale'
# mkdir 'all_supernovae/plots/wavelength'

rm types.txt

echo "Done making necessary directories" 