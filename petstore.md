<a id="swagger-petstore-api"></a># Swagger Petstore API

Version: 1\.0\.7

This is a sample server Petstore server\. You can find out more about Swagger at [http://swagger\.io](http://swagger.io) or on [irc\.freenode\.net, \#swagger](http://swagger.io/irc/)\. For this sample, you can use the api key special\-key to test the authorization filters\.

__Base URL:__ https://petstore\.swagger\.io/v2

<a id="authentication"></a>## Authentication

This API uses the following authentication schemes: \- API Key \(api\_key\): API key authentication \- OAuth 2\.0 \(petstore\_auth\): Implicit flow with the following scopes: \- read:pets: read your pets \- write:pets: modify pets in your account

<a id="endpoints"></a>## Endpoints

<a id="pet"></a>### Pet

<a id="upload-an-image"></a>#### Upload an image

- __POST__ /pet/\{petId\}/uploadImage
- __Description:__ Uploads an image
- __Parameters:__
	- petId \(path, required\): ID of pet to update
	- additionalMetadata \(formData, optional\): Additional data to pass to server
	- file \(formData, optional\): file to upload
- __Responses:__
	- 200: successful operation

<a id="add-a-new-pet-to-the-store"></a>#### Add a new pet to the store

- __POST__ /pet
- __Description:__ Add a new pet to the store
- __Parameters:__
	- body \(body, required\): Pet object that needs to be added to the store
- __Responses:__
	- 405: Invalid input

<a id="update-an-existing-pet"></a>#### Update an existing pet

- __PUT__ /pet
- __Description:__ Update an existing pet
- __Parameters:__
	- body \(body, required\): Pet object that needs to be added to the store
- __Responses:__
	- 400: Invalid ID supplied
	- 404: Pet not found
	- 405: Validation exception

<a id="finds-pets-by-status"></a>#### Finds Pets by status

- __GET__ /pet/findByStatus
- __Description:__ Multiple status values can be provided with comma separated strings
- __Parameters:__
	- status \(query, required\): Status values that need to be considered for filter
- __Responses:__
	- 200: successful operation
	- 400: Invalid status value

<a id="finds-pets-by-tags-deprecated"></a>#### Finds Pets by tags \(deprecated\)

- __GET__ /pet/findByTags
- __Description:__ Multiple tags can be provided with comma separated strings\. Use tag1, tag2, tag3 for testing\.
- __Parameters:__
	- tags \(query, required\): Tags to filter by
- __Responses:__
	- 200: successful operation
	- 400: Invalid tag value

<a id="find-pet-by-id"></a>#### Find pet by ID

- __GET__ /pet/\{petId\}
- __Description:__ Returns a single pet
- __Parameters:__
	- petId \(path, required\): ID of pet to return
- __Responses:__
	- 200: successful operation
	- 400: Invalid ID supplied
	- 404: Pet not found

<a id="X9ab0ce49d57dd6f44beccc6a8a87379a2f015bb"></a>#### Updates a pet in the store with form data

- __POST__ /pet/\{petId\}
- __Description:__ Updates a pet in the store with form data
- __Parameters:__
	- petId \(path, required\): ID of pet that needs to be updated
	- name \(formData, optional\): Updated name of the pet
	- status \(formData, optional\): Updated status of the pet
- __Responses:__
	- 405: Invalid input

<a id="deletes-a-pet"></a>#### Deletes a pet

- __DELETE__ /pet/\{petId\}
- __Description:__ Deletes a pet
- __Parameters:__
	- api\_key \(header, optional\): API key
	- petId \(path, required\): Pet id to delete
- __Responses:__
	- 400: Invalid ID supplied
	- 404: Pet not found

<a id="store"></a>### Store

<a id="returns-pet-inventories-by-status"></a>#### Returns pet inventories by status

- __GET__ /store/inventory
- __Description:__ Returns a map of status codes to quantities
- __Responses:__
	- 200: successful operation

<a id="place-an-order-for-a-pet"></a>#### Place an order for a pet

- __POST__ /store/order
- __Description:__ Place an order for a pet
- __Parameters:__
	- body \(body, required\): order placed for purchasing the pet
- __Responses:__
	- 200: successful operation
	- 400: Invalid Order

<a id="find-purchase-order-by-id"></a>#### Find purchase order by ID

- __GET__ /store/order/\{orderId\}
- __Description:__ For valid response try integer IDs with value >= 1 and <= 10\. Other values will generated exceptions
- __Parameters:__
	- orderId \(path, required\): ID of pet that needs to be fetched
- __Responses:__
	- 200: successful operation
	- 400: Invalid ID supplied
	- 404: Order not found

<a id="delete-purchase-order-by-id"></a>#### Delete purchase order by ID

- __DELETE__ /store/order/\{orderId\}
- __Description:__ For valid response try integer IDs with positive integer value\. Negative or non\-integer values will generate API errors
- __Parameters:__
	- orderId \(path, required\): ID of the order that needs to be deleted
- __Responses:__
	- 400: Invalid ID supplied
	- 404: Order not found

<a id="user"></a>### User

<a id="create-user"></a>#### Create user

- __POST__ /user
- __Description:__ This can only be done by the logged in user\.
- __Parameters:__
	- body \(body, required\): Created user object
- __Responses:__
	- default: successful operation

<a id="X0c1198a04da81196758478f2676b7a6d8d5ca19"></a>#### Creates list of users with given input array

- __POST__ /user/createWithArray
- __Description:__ Creates list of users with given input array
- __Parameters:__
	- body \(body, required\): List of user object
- __Responses:__
	- default: successful operation

<a id="X516e94d8568d880dcbcda8358c9784abb3972a7"></a>#### Creates list of users with given input array

- __POST__ /user/createWithList
- __Description:__ Creates list of users with given input array
- __Parameters:__
	- body \(body, required\): List of user object
- __Responses:__
	- default: successful operation

<a id="logs-user-into-the-system"></a>#### Logs user into the system

- __GET__ /user/login
- __Description:__ Logs user into the system
- __Parameters:__
	- username \(query, required\): The user name for login
	- password \(query, required\): The password for login in clear text
- __Responses:__
	- 200: successful operation
	- 400: Invalid username/password supplied

<a id="logs-out-current-logged-in-user-session"></a>#### Logs out current logged in user session

- __GET__ /user/logout
- __Description:__ Logs out current logged in user session
- __Responses:__
	- default: successful operation

<a id="get-user-by-user-name"></a>#### Get user by user name

- __GET__ /user/\{username\}
- __Description:__ Get user by user name
- __Parameters:__
	- username \(path, required\): The name that needs to be fetched\. Use user1 for testing\.
- __Responses:__
	- 200: successful operation
	- 400: Invalid username supplied
	- 404: User not found

<a id="updated-user"></a>#### Updated user

- __PUT__ /user/\{username\}
- __Description:__ This can only be done by the logged in user\.
- __Parameters:__
	- username \(path, required\): name that need to be updated
	- body \(body, required\): Updated user object
- __Responses:__
	- 400: Invalid user supplied
	- 404: User not found

<a id="delete-user"></a>#### Delete user

- __DELETE__ /user/\{username\}
- __Description:__ This can only be done by the logged in user\.
- __Parameters:__
	- username \(path, required\): The name that needs to be deleted
- __Responses:__
	- 400: Invalid username supplied
	- 404: User not found

<a id="models"></a>## Models

<a id="apiresponse"></a>### ApiResponse

- code \(integer, int32\)
- type \(string\)
- message \(string\)

<a id="category"></a>### Category

- id \(integer, int64\)
- name \(string\)

<a id="pet-1"></a>### Pet

- id \(integer, int64\)
- category \(Category\)
- name \(string, required\)
- photoUrls \(array of strings, required\)
- tags \(array of Tag\)
- status \(string, enum: available, pending, sold\)

<a id="tag"></a>### Tag

- id \(integer, int64\)
- name \(string\)

<a id="order"></a>### Order

- id \(integer, int64\)
- petId \(integer, int64\)
- quantity \(integer, int32\)
- shipDate \(string, date\-time\)
- status \(string, enum: placed, approved, delivered\)
- complete \(boolean\)

<a id="user-1"></a>### User

- id \(integer, int64\)
- username \(string\)
- firstName \(string\)
- lastName \(string\)
- email \(string\)
- password \(string\)
- phone \(string\)
- userStatus \(integer, int32\)

<a id="external-documentation"></a>## External Documentation

Find out more about Swagger: [http://swagger\.io](http://swagger.io)

