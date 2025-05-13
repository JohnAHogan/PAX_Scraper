
class JobPosting:
    def __init__(self, job_ref, listing_data):
        self.job_ref = job_ref
        self.listing_data = listing_data.get_attribute("innerHTML")

    def get_URL(self):
        return self.job_ref
    
    def get_data(self):
        return self.listing_data