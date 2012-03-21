from logger import log
from skely import SkelYaml
from skel import Skel

#this tuple holds the possible filetypes for a skeleton object, and is used by
#the language module's load_directives method.
SKEL_TYPES = (
    'xml',
    'yaml'
)

def create_skel(filename):
    """returns appropriate Skel-type object based on file name

    examples:
        filename "skel.yaml" will return a SkelYaml object
        filename "skel.xml" will return a Skel object

    """
    log.debug('create_skel: Attempting to create new skeleton')
    if filename[-4:] == 'yaml':
        log.debug('create_skel: Creating new yaml skeleton from file: ' + filename)
        return SkelYaml(filename)

    if filename[-3:] == 'xml':
        log.debug('create_skel: Creating new xml skeleton from file: ' + filename)
        return Skel(filename)

