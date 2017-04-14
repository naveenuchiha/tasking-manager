from server import db
from server.models.dtos.tags_dto import TagsDTO


class Tags(db.Model):
    """ Describes an individual mapping Task """
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    organisations = db.Column(db.String, unique=True)
    campaigns = db.Column(db.String, unique=True)

    @staticmethod
    def upsert_organistion_tag(organisation_tag: str) -> str:
        """ Insert organisation tag if it doesn't exists otherwise return matching tag """
        org_tag = Tags.query.filter_by(organisations=organisation_tag.lower()).one_or_none()

        if org_tag is not None:
            return org_tag

        tag = Tags()
        tag.organisations = organisation_tag.lower()
        db.session.add(tag)  # Note no commit here, done as part of project update transaction
        return organisation_tag.lower()

    @staticmethod
    def upsert_campaign_tag(campaign_tag: str) -> str:
        """ Insert campaign tag if doesn't exist otherwise return matching tag"""
        camp_tag = Tags.query.filter_by(campaigns=campaign_tag.lower()).one_or_none()

        if camp_tag is not None:
            return camp_tag

        tag = Tags()
        tag.campaigns = campaign_tag.lower()
        db.session.add(tag)  # Note no commit here, done as part of project update transaction
        return campaign_tag.lower()

    @staticmethod
    def get_all_organisations():
        """ Get all org tags in DB """
        result = db.session.query(Tags.organisations).filter(Tags.organisations.isnot(None))

        dto = TagsDTO()
        dto.tags = [r for r, in result]
        return dto

    @staticmethod
    def get_all_campaigns():
        """ Get all campaign tags in DB """
        result = db.session.query(Tags.campaigns).filter(Tags.campaigns.isnot(None))

        dto = TagsDTO()
        dto.tags = [r for r, in result]
        return dto