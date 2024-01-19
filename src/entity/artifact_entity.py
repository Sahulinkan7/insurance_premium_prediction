from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    downloaded_data_filepath: str
    extracted_data_filepath: str
    trained_data_filepath: str
    test_data_filepath: str
