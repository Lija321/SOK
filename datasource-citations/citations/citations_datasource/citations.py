import os
from typing import List, Dict, Set
from datetime import datetime

# Import from the installed citations package
from citations.api.model import Citation, Author
from citations.api.services import DataSourcePlugin


class CitationsDatasource(DataSourcePlugin):
    def __init__(self, data_dir: str = None):
        """
        Initialize the Citations Datasource.
        
        :param data_dir: Directory containing the citation data files.
        """
        if data_dir is None:
            # Default to the data directory relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up two directories: citations_datasource -> citations -> datasource-citations
            data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data')
        
        self.data_dir = data_dir
        self.citations_file = os.path.join(data_dir, 'Cit-HepTh.txt')
        self.dates_file = os.path.join(data_dir, 'Cit-HepTh-dates.txt')
        self.abstracts_dir = os.path.join(data_dir, 'cit-HepTh-abstracts')
        
        # Cache for loaded data
        self._citations_cache: Dict[str, Citation] = {}
        self._dates_cache: Dict[str, datetime] = {}
        self._citation_relationships: Dict[str, Set[str]] = {}
        self._abstracts_cache: Dict[str, Dict[str, str]] = {}
        self._loaded = False

    def name(self) -> str:
        return "High Energy Physics Theory Citations Datasource"

    def identifier(self) -> str:
        return "datasource_hep_th_citations"
    
    def _load_dates(self) -> Dict[str, datetime]:
        """Load publication dates from the dates file."""
        if self._dates_cache:
            return self._dates_cache
            
        dates = {}
        try:
            with open(self.dates_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('\t')
                        if len(parts) == 2:
                            paper_id, date_str = parts
                            try:
                                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                                dates[paper_id] = date_obj
                            except ValueError:
                                continue
        except FileNotFoundError:
            print(f"Warning: Dates file not found at {self.dates_file}")
        
        self._dates_cache = dates
        return dates
    
    def _load_citation_relationships(self) -> Dict[str, Set[str]]:
        """Load citation relationships from the citations file."""
        if self._citation_relationships:
            return self._citation_relationships
            
        relationships = {}
        try:
            with open(self.citations_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('\t')
                        if len(parts) == 2:
                            citing_paper, cited_paper = parts
                            if citing_paper not in relationships:
                                relationships[citing_paper] = set()
                            relationships[citing_paper].add(cited_paper)
        except FileNotFoundError:
            print(f"Warning: Citations file not found at {self.citations_file}")
        
        self._citation_relationships = relationships
        return relationships
    
    def _load_abstract_info(self, paper_id: str) -> Dict[str, str]:
        """Load abstract information for a specific paper ID."""
        if paper_id in self._abstracts_cache:
            return self._abstracts_cache[paper_id]
        
        # Determine the year from the paper ID (first 2 digits after 92)
        if len(paper_id) >= 4 and paper_id.startswith('92'):
            year = f"19{paper_id[:2]}"
        elif len(paper_id) >= 4 and paper_id.startswith(('93', '94', '95', '96', '97', '98', '99')):
            year = f"19{paper_id[:2]}"
        elif len(paper_id) >= 4 and paper_id.startswith(('00', '01', '02', '03')):
            year = f"20{paper_id[:2]}"
        else:
            return {}
        
        abstract_file = os.path.join(self.abstracts_dir, year, f"{paper_id}.abs")
        
        if not os.path.exists(abstract_file):
            return {}
        
        try:
            with open(abstract_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            info = {}
            lines = content.split('\n')
            
            # Parse the abstract file
            for i, line in enumerate(lines):
                line_stripped = line.strip()
                
                # Extract arXiv paper ID
                if line_stripped.startswith('Paper:'):
                    arxiv_match = line_stripped.replace('Paper:', '').strip()
                    info['arxiv_id'] = arxiv_match
                
                # Extract submitter email
                elif line_stripped.startswith('From:'):
                    from_line = line_stripped[5:].strip()
                    # Extract email from formats like "email@domain.com (Name)" or just "email@domain.com"
                    import re
                    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', from_line)
                    if email_match:
                        info['submitter_email'] = email_match.group(1)
                    
                # Extract submission date
                elif line_stripped.startswith('Date:'):
                    date_line = line_stripped[5:].strip()
                    # Parse various date formats
                    try:
                        # Try to extract date from complex formats
                        import re
                        # Look for patterns like "Tue Dec 31 23:54:17 MET 1991"
                        date_parts = date_line.split()
                        if len(date_parts) >= 4:
                            # Try to find year
                            year_match = re.search(r'(19|20)\d{2}', date_line)
                            if year_match:
                                info['submission_date_raw'] = date_line
                                info['submission_year'] = int(year_match.group())
                    except:
                        pass
                
                elif line_stripped.startswith('Title:'):
                    info['title'] = line_stripped[6:].strip()
                elif line_stripped.startswith('Authors:'):
                    info['authors'] = line_stripped[8:].strip()
                elif line_stripped.startswith('Comments:'):
                    info['comments'] = line_stripped[9:].strip()
                elif line_stripped.startswith('Subj-class:'):
                    info['subject_class'] = line_stripped[11:].strip()
                elif line_stripped.startswith('Journal-ref:'):
                    info['journal'] = line_stripped[12:].strip()
                elif line_stripped.startswith('DOI:'):
                    info['doi'] = line_stripped[4:].strip()
                elif line_stripped == '\\\\':
                    # Abstract starts after \\
                    abstract_lines = lines[i+1:]
                    # Remove empty lines and join
                    abstract_text = ' '.join([l.strip() for l in abstract_lines if l.strip() and not l.strip().startswith('\\\\')])
                    # Clean up the abstract text
                    abstract_text = ' '.join(abstract_text.split())  # Normalize whitespace
                    info['abstract'] = abstract_text
                    break
            
            self._abstracts_cache[paper_id] = info
            return info
            
        except Exception as e:
            print(f"Warning: Could not parse abstract file for {paper_id}: {e}")
            return {}
    
    def _parse_authors(self, authors_string: str) -> List[Author]:
        """Parse authors string into Author objects."""
        if not authors_string:
            return [Author(id="unknown", first_name="Unknown", last_name="Author")]
        
        import re
        authors = []
        
        # Split by 'and' or comma, but be careful with initials
        # Replace common separators
        authors_clean = authors_string.replace(' and ', ', ')
        
        # Split by comma but handle initials properly
        author_parts = []
        current_part = ""
        
        for char in authors_clean:
            if char == ',' and len(current_part.strip()) > 3:  # Avoid splitting on initials
                author_parts.append(current_part.strip())
                current_part = ""
            else:
                current_part += char
        
        if current_part.strip():
            author_parts.append(current_part.strip())
        
        for i, author_part in enumerate(author_parts):
            author_part = author_part.strip()
            if not author_part:
                continue
            
            # Generate a unique but deterministic ID
            author_id = f"author_{abs(hash(author_part)) % 1000000}"
            
            # Handle different name formats
            if '.' in author_part and len(author_part.split()) <= 3:
                # Likely has initials: "F.Bonechi", "C. Itzykson", "J.-B. Zuber"
                parts = author_part.split()
                if len(parts) == 1:
                    # Format like "F.Bonechi"
                    match = re.match(r'([A-Z]+\.[-]?[A-Z]*\.?)(.+)', author_part)
                    if match:
                        initials = match.group(1)
                        last_name = match.group(2)
                        first_name = initials.replace('.', '').replace('-', ' ')
                    else:
                        first_name = author_part
                        last_name = ""
                        initials = None
                else:
                    # Format like "C. Itzykson" or "J.-B. Zuber"
                    potential_initials = parts[0]
                    last_name = ' '.join(parts[1:])
                    first_name = potential_initials.replace('.', '').replace('-', ' ')
                    initials = potential_initials
            else:
                # Full names: "Claude Itzykson"
                name_parts = author_part.split()
                if len(name_parts) >= 2:
                    first_name = ' '.join(name_parts[:-1])
                    last_name = name_parts[-1]
                    initials = None
                else:
                    first_name = author_part
                    last_name = ""
                    initials = None
            
            author = Author(
                id=author_id,
                first_name=first_name,
                last_name=last_name,
                initials=initials
            )
            authors.append(author)
        
        return authors if authors else [Author(id="unknown", first_name="Unknown", last_name="Author")]
    
    def _create_citation_from_id(self, paper_id: str, dates: Dict[str, datetime], 
                                relationships: Dict[str, Set[str]]) -> Citation:
        """Create a Citation object from a paper ID."""
        # Get publication date
        pub_date = dates.get(paper_id)
        pub_year = pub_date.year if pub_date else None
        
        # Load abstract information if available
        abstract_info = self._load_abstract_info(paper_id)
        
        # Get title from abstract or generate default
        title = abstract_info.get('title', f"High Energy Physics Theory Paper {paper_id}")
        
        # Parse authors from abstract or create default
        authors_string = abstract_info.get('authors', '')
        authors = self._parse_authors(authors_string)
        
        # Get journal information
        journal = abstract_info.get('journal', "arXiv High Energy Physics - Theory")
        
        # Get abstract text
        abstract_text = abstract_info.get('abstract', '')
        
        # Get additional metadata
        doi = abstract_info.get('doi', None)
        subject_class = abstract_info.get('subject_class', None)
        comments = abstract_info.get('comments', None)
        arxiv_id = abstract_info.get('arxiv_id', None)
        submitter_email = abstract_info.get('submitter_email', None)
        
        # Handle submission date
        submission_date = None
        submission_year = abstract_info.get('submission_year')
        if submission_year:
            try:
                # Create a basic datetime object with just the year
                submission_date = datetime(submission_year, 1, 1)
            except:
                pass
        
        # Use submission year if no publication year available
        if not pub_year and submission_year:
            pub_year = submission_year
        
        return Citation(
            id=paper_id,
            title=title,
            authors=authors,
            publication_year=pub_year,
            submission_date=submission_date,
            journal=journal,
            doi=doi,
            abstract=abstract_text,
            subject_class=subject_class,
            comments=comments,
            arxiv_id=arxiv_id,
            submitter_email=submitter_email,
            url=f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else f"https://arxiv.org/abs/hep-th/{paper_id}"
        )
    
    def load(self, **kwargs) -> List[Citation]:
        """Load all citations from the data source."""
        if self._loaded and self._citations_cache:
            return list(self._citations_cache.values())
        
        dates = self._load_dates()
        relationships = self._load_citation_relationships()
        
        # Get all unique paper IDs
        all_paper_ids = set(dates.keys())
        all_paper_ids.update(relationships.keys())
        for cited_papers in relationships.values():
            all_paper_ids.update(cited_papers)
        
        # Create Citation objects
        citations = {}
        for paper_id in all_paper_ids:
            citation = self._create_citation_from_id(paper_id, dates, relationships)
            citations[paper_id] = citation
        
        self._citations_cache = citations
        self._loaded = True
        
        # Apply any filtering from kwargs
        limit = kwargs.get('limit')
        if limit and isinstance(limit, int):
            return list(citations.values())[:limit]
        
        return list(citations.values())
    
    def search(self, query: str, **kwargs) -> List[Citation]:
        """Search for citations based on a query string."""
        if not self._loaded:
            self.load()
        
        query_lower = query.lower()
        results = []
        
        for citation in self._citations_cache.values():
            # Search in title, authors, and paper ID
            if (query_lower in citation.title.lower() or
                query_lower in citation.authors_string.lower() or
                query_lower in citation.id):
                results.append(citation)
        
        # Apply any filtering from kwargs
        limit = kwargs.get('limit')
        if limit and isinstance(limit, int):
            return results[:limit]
        
        return results
    
    def get_by_id(self, citation_id: str, **kwargs) -> Citation:
        """Retrieve a specific citation by its ID."""
        if not self._loaded:
            self.load()
        
        citation = self._citations_cache.get(citation_id)
        if citation is None:
            raise ValueError(f"Citation with ID '{citation_id}' not found")
        
        return citation
    
    def get_citations_by_author(self, author_name: str, **kwargs) -> List[Citation]:
        """Get all citations by a specific author."""
        return self.search(author_name, **kwargs)
    
    def get_citations_by_year(self, year: int, **kwargs) -> List[Citation]:
        """Get all citations from a specific year."""
        if not self._loaded:
            self.load()
        
        results = []
        for citation in self._citations_cache.values():
            if citation.publication_year == year:
                results.append(citation)
        
        return results
    
    def get_citation_relationships(self, paper_id: str) -> Dict[str, List[str]]:
        """Get citation relationships for a specific paper."""
        relationships = self._load_citation_relationships()
        
        # Papers this paper cites
        cites = list(relationships.get(paper_id, set()))
        
        # Papers that cite this paper
        cited_by = []
        for citing_paper, cited_papers in relationships.items():
            if paper_id in cited_papers:
                cited_by.append(citing_paper)
        
        return {
            'cites': cites,
            'cited_by': cited_by
        }