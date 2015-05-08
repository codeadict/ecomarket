class LeadSources:
    GATE_MODAL = 'HM'
    BLOG_POPUP = 'BP'
    DATA_COLLECTION = 'DC'
    GOOGLE_CPC = 'CC'
    REGISTER_PAGE = 'RP'
    PRODUCT_GIVEAWAY = 'PG'
    UNKNOWN = 'UK'  # unused


class MemberTypes:
    NORMAL = 0
    SELLER = 1
    SELLER_LEAD = 2  # unused


class BatchStatus:
    NEW = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3

    @classmethod
    def from_api_text(cls, text):
        """Get the numeric status from the text returned by the API"""
        return {
            "completed": cls.COMPLETED,
            "pending": cls.IN_PROGRESS,
            "error": cls.FAILED,
        }[text]
