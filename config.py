class Config:
    # Model settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 80MB, fast
    MODEL_CACHE_DIR = "./models/model_cache"
    MAX_MODEL_SIZE = 1024 * 1024 * 1024  # 1GB in bytes
    
    # Processing settings
    MAX_PROCESSING_TIME = 60  # seconds
    MAX_SECTION_LENGTH = 2000  # characters
    MIN_SECTION_LENGTH = 50
    
    # Scoring weights
    PERSONA_WEIGHT = 0.4
    JOB_WEIGHT = 0.6
    
    # Output settings
    MAX_SECTIONS = 10
    MAX_SUBSECTIONS = 5