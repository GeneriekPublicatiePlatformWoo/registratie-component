from collections import defaultdict

from django.db.models.query import ModelIterable

from treebeard.mp_tree import MP_Node, MP_NodeManager, MP_NodeQuerySet


class ChildThemesIterable(ModelIterable):
    def __iter__(self):
        model_cls = self.queryset.model
        assert issubclass(model_cls, MP_Node)

        _children = defaultdict(list)

        for obj in super().__iter__():
            parentpath = obj._get_basepath(obj.path, obj.depth - 1)
            _children[parentpath].append(obj)

        shorted_keys_first = sorted(_children.keys(), key=lambda k: len(k))
        if not shorted_keys_first:
            return

        def _assign_children(theme):
            theme.sub_themes = _children[theme.path]
            for child in theme.sub_themes:
                _assign_children(child)

        len_shortest_key = len(shorted_keys_first[0])
        for key in shorted_keys_first:
            if len(key) > len_shortest_key:
                break

            for node in _children[key]:
                _assign_children(node)
                yield node


class CustomMP_NodeQuerySet(MP_NodeQuerySet):
    """
    Custom queryset which adds optimized tree dumping.
    """

    # _as_tree: bool = False

    # def _clone(self):
    #     clone = super()._clone()
    #     clone._as_tree = self._as_tree
    #     return clone

    def as_tree(self, parent=None):
        """
        Inspired by MP_Node.dump_bulk, optimize querying and dumping a tree structure.

        We split the query in two querysets:

        1. the main queryset, which applies the filter parameters and where clauses etc.
        2. the children queryset, which grabs the possible paths from the main qs and
           retrieves only the relevant children.

        We then stitch together these result sets, similar to prefetch_related so that
        we have a fixed number of optimized queries to get result sets *with* children.
        """
        self._iterable_class = ChildThemesIterable
        # if no parent is provided, we only consider root nodes
        _filters = {"path__startswith": parent.path} if parent else {"depth": 1}
        qs = self.filter(**_filters)

        # main_qs = self
        # children_qs = self.filter(path__startswith=main_qs.values("path"))

        # breakpoint()
        return qs


class CustomMP_NodeManager(MP_NodeManager):
    """
    Custom manager that exposes our custom queryset with additional functionality.
    """

    def get_queryset(self):
        return CustomMP_NodeQuerySet(self.model).order_by("path")

    def as_tree(self):
        return self.get_queryset().as_tree()
