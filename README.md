## Serializers
<p>  Serializers are the python program that converts complex models objects and instances to json and vice versa 
<br>
In django all the data are stored in complex data objects but when we have to interact with frontend the interaction is done with the 
help of json or xml but we use json in django.
so we need a mechanism to convert these complex model objects into json and this is done by serializers
</p>
<h1> some of the things we need to know about serializers </h1>
<p> we can define a function called validate in serializers that is accessed by view using object.is_valid() </p>
<p> we define a function called create in serializers which is accessed in valid using object.save() </p>