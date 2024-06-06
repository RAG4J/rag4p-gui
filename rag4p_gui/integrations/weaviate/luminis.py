import weaviate.classes.config as wvc

additional_properties = [
    wvc.Property(name="title",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="updated_at",
                 data_type=wvc.DataType.DATE,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="url",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="body",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="categories",
                 data_type=wvc.DataType.TEXT_ARRAY,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="tags",
                 data_type=wvc.DataType.TEXT_ARRAY,
                 vectorize_property_name=False,
                 skip_vectorization=True),
]

additional_properties_short = ['title', 'updated_at', 'url', 'categories', 'tags']