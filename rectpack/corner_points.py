from rectpack.skyline import Skyline


class CornerPoints(Skyline):
    # TODO implement right view apart from the top view
    # TODO implement similar version for MaxRects
    def _select_position(self, width, height):
        """
        Search for the placement with the bes fitness for the rectangle.

        Returns:
            tuple (Rectangle, fitness) - Rectangle placed in the fittest position
            None - Rectangle couldn't be placed
        """
        positions = self._generate_placements(width, height)
        if self.rot and width != height:
            positions += self._generate_placements(height, width)
        if not positions:
            return None, None
        return [p[0] for p in positions], None

    def select_best_position(self, width, height):
        if self._waste_management:
            raise NotImplementedError("Waste management depends on Guillotine, which is not easly separable")

        assert (width > 0 and height > 0)
        if width > max(self.width, self.height) or \
                height > max(self.height, self.width):
            return None

        rects, _ = self._select_position(width, height)

        return list(rects)
