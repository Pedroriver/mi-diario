import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="d3quh5ss",
    api_key="585578171832242",
    api_secret="JBPN22GSLWSJl6R7amzoUqfhH4g",
    secure=True
)

# Subimos una imagen de prueba de internet
resultado = cloudinary.uploader.upload(
    "https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
    public_id="prueba_diario"
)
print("¡Éxito! La imagen está en:", resultado["secure_url"])
