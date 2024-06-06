import weaviate.classes.config as wvc

additional_properties = [
    wvc.Property(name="title",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="time",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="room",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="speakers",
                 data_type=wvc.DataType.TEXT_ARRAY,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="tags",
                 data_type=wvc.DataType.TEXT_ARRAY,
                 vectorize_property_name=False,
                 skip_vectorization=True),
]
