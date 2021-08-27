The generate_nametags.sh script reads a guest text file (the same format that
is generated from the django admin update_guestlist script), generates a QR
code, and composites the name data with a QR code on the nametag template.

It depends on the imagemagick and qrencode packages.
