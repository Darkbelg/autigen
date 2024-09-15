# Functional Specs

## Upload image
### REQUEST 
#### URL
POST: https://example.test/pet/{petId}/uploadImage
#### Body
petId integer
file formdata

#### Response
200 petId

## Upload image
### REQUEST 
#### URL
GET: https://example.test/pet

#### Response
{
  "id": 0,
  "category": {
    "id": 0,
    "name": "string"
  },
  "name": "doggie",
  "photoUrls": [
    "string"
  ],
  "tags": [
    {
      "id": 0,
      "name": "string"
    }
  ],
  "status": "available"
}
