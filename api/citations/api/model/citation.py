from typing import List, Optional
from datetime import datetime
from .author import Author


class Citation(object):
    def __init__(self, 
                 id: str,
                 title: str,
                 authors: List[Author],
                 publication_year: Optional[int] = None,
                 submission_date: Optional[datetime] = None,
                 journal: Optional[str] = None,
                 volume: Optional[str] = None,
                 issue: Optional[str] = None,
                 pages: Optional[str] = None,
                 doi: Optional[str] = None,
                 url: Optional[str] = None,
                 abstract: Optional[str] = None,
                 subject_class: Optional[str] = None,
                 comments: Optional[str] = None,
                 arxiv_id: Optional[str] = None,
                 submitter_email: Optional[str] = None):
        self.__id = id
        self.__title = title
        self.__authors = authors
        self.__publication_year = publication_year
        self.__submission_date = submission_date
        self.__journal = journal
        self.__volume = volume
        self.__issue = issue
        self.__pages = pages
        self.__doi = doi
        self.__url = url
        self.__abstract = abstract
        self.__subject_class = subject_class
        self.__comments = comments
        self.__arxiv_id = arxiv_id
        self.__submitter_email = submitter_email

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: str):
        if isinstance(value, str):
            self.__id = value
        else:
            raise TypeError('Value must be type of str')

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str):
        if isinstance(value, str):
            self.__title = value
        else:
            raise TypeError('Value must be type of str')

    @property
    def authors(self):
        return self.__authors

    @authors.setter
    def authors(self, value: List[Author]):
        if isinstance(value, list):
            self.__authors = value
        else:
            raise TypeError('Value must be type of List[Author]')

    @property
    def publication_year(self):
        return self.__publication_year

    @publication_year.setter
    def publication_year(self, value: int):
        if isinstance(value, int):
            self.__publication_year = value
        else:
            raise TypeError('Value must be type of int')

    @property
    def journal(self):
        return self.__journal

    @journal.setter
    def journal(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__journal = value

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__volume = value

    @property
    def issue(self):
        return self.__issue

    @issue.setter
    def issue(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__issue = value

    @property
    def pages(self):
        return self.__pages

    @pages.setter
    def pages(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__pages = value

    @property
    def doi(self):
        return self.__doi

    @doi.setter
    def doi(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__doi = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__url = value

    @property
    def abstract(self):
        return self.__abstract

    @abstract.setter
    def abstract(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__abstract = value

    @property
    def submission_date(self):
        return self.__submission_date

    @submission_date.setter
    def submission_date(self, value: datetime):
        if value is not None and not isinstance(value, datetime):
            raise TypeError('Value must be type of datetime or None')
        self.__submission_date = value

    @property
    def subject_class(self):
        return self.__subject_class

    @subject_class.setter
    def subject_class(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__subject_class = value

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__comments = value

    @property
    def arxiv_id(self):
        return self.__arxiv_id

    @arxiv_id.setter
    def arxiv_id(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__arxiv_id = value

    @property
    def submitter_email(self):
        return self.__submitter_email

    @submitter_email.setter
    def submitter_email(self, value: str):
        if value is not None and not isinstance(value, str):
            raise TypeError('Value must be type of str or None')
        self.__submitter_email = value

    @property
    def authors_string(self):
        return ", ".join([author.full_name for author in self.__authors])

    @property
    def formatted_citation(self):
        """Get a properly formatted citation string."""
        citation_parts = []
        
        # Authors
        citation_parts.append(self.authors_string)
        
        # Year
        if self.publication_year:
            citation_parts.append(f"({self.publication_year})")
        elif self.submission_date:
            citation_parts.append(f"({self.submission_date.year})")
        
        # Title
        citation_parts.append(f"{self.title}.")
        
        # Journal
        if self.journal:
            citation_parts.append(self.journal)
        
        # ArXiv ID
        if self.arxiv_id:
            citation_parts.append(f"arXiv:{self.arxiv_id}")
        
        return " ".join(citation_parts)

    def __str__(self):
        return self.formatted_citation
