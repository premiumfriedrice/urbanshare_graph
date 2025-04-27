from PIL import Image
import piexif

def exif_from_bytes(exif_dict):
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    exif_tag_dict['thumbnail'] = thumbnail.decode("ISO-8859-1")

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode("ISO-8859-1")

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict

def getDegrees(value) -> float:
    d = value[0][0] / value[0][1]
    m = value[1][0] / value[1][1] / 60.0
    s = value[2][0] / value[2][1] / 3600.0
    return d + m + s

def getLocation(image_file_path : str) -> dict:
    result = {}
    
    img = Image.open(image_file_path)
    
    exif_data = piexif.load(img.info.get("exif"))
    exif_data = exif_from_bytes(exif_data)
    gps_data = exif_data["GPS"]
    
    latitude_ref = gps_data["GPSLatitudeRef"]
    longitude_ref = gps_data["GPSLongitudeRef"]
    latitude = getDegrees(gps_data["GPSLatitude"])
    longitude = getDegrees(gps_data["GPSLongitude"])
    
    if latitude_ref != "N":
        latitude *= -1
    if longitude_ref != "E":
        longitude *= -1
        
    return latitude, longitude

if __name__ == "__main__":
    print(getLocation("TestImage.jpeg"))