import weaviate.classes.config as wvc

additional_properties = [
    wvc.Property(name="title",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="published_at",
                 data_type=wvc.DataType.DATE,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="url",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="author",
                 data_type=wvc.DataType.TEXT,
                 vectorize_property_name=False,
                 skip_vectorization=True),
    wvc.Property(name="tags",
                 data_type=wvc.DataType.TEXT_ARRAY,
                 vectorize_property_name=False,
                 skip_vectorization=True),
]

additional_properties_short = ['title', 'published_at', 'url', 'author', 'tags']