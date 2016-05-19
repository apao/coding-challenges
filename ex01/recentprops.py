import heapq

DEFAULT_MAX_SIZE = 100


class RecentProperties(object):
    """Object that represents recently viewed properties."""

    def __init__(self, max_size=DEFAULT_MAX_SIZE):
        self.pq = []
        self.id_finder = {}
        self.counter = 0
        self.max_size = max_size


    def add_property(self, property_id):
        """Add a recently viewed property."""

        self.counter += 1

        # TRY IF PROPERTY ID IS INT OR CAN BE COVERTED INTO AN INT
        try:
            prop_id = int(property_id)
            # PROPERTY ID IS IN FINDER
            if prop_id in self.id_finder:
                property_details = self.id_finder.get(prop_id)
                property_details.update_count(self.counter)
                heapq.heapify(self.pq)
            else:  # PROPERTY ID NOT IN FINDER
                # MAX SIZE HAS BEEN REACHED
                if len(self.id_finder) == self.max_size:  # LIMITS SIZE OF ID FINDER TO PRE-DETERMINED MAX SIZE
                    # REMOVE OLDEST VIEWED DETAILS OBJECT FROM PQ
                    property_removed = self._pop_property()
                    # REMOVE OLDEST VIEWED PROPERTY ID FROM FINDER
                    del self.id_finder[property_removed.prop_id]
                # INSTANTIATE NEW DETAILS OBJECT
                new_property = PropertyDetails(prop_id, self.counter)
                # ADD NEW DETAILS OBJECT TO PQ - HEAPPUSH MAINTAINS THE HEAP INVARIANT
                heapq.heappush(self.pq, new_property)
                # ADD NEW ID AND DETAILS OBJECT TO FINDER
                self.id_finder[prop_id] = new_property
        # RAISE ERRORS OTHERWISE
        except ValueError:
            print "Invalid property ID - must be able to convert into integer."
            raise
        except TypeError:
            print "Invalid property ID - must not be None."
            raise

    def most_recent(self):
        """Return, not in any particular order, the unique property IDs of up to the 100 most recently added/streamed properties."""

        return self.id_finder.keys()

    def _pop_property(self):
        """Helper method to remove the lowest count (oldest viewed) object from the min heap and return it."""

        prop_details_obj = heapq.heappop(self.pq)
        return prop_details_obj


class PropertyDetails(object):
    """Object that represents a single property."""

    def __init__(self, property_id=None, count=None):
        """Create a PropertyDetails object."""

        self.prop_id = property_id
        self.count = count

    def __repr__(self):
        """Overwrite existing repr method."""

        return "<%s: ID %s, count %s>" % (self.__class__.__name__,
                                          self.prop_id,
                                          self.count)

    def __lt__(self, other):
        """Custom overwrite existing less than comparison to reference count attribute because heapq uses __lt__ to maintain min heap invariance."""

        return self.count < other.count

    def update_count(self, count):
        """Update count of details object."""

        self.count = count
