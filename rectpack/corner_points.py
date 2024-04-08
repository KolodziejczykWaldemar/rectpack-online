from rectpack.geometry import Rectangle
from rectpack.maxrects import MaxRects
from rectpack.skyline import Skyline


class CornerPointsMR(MaxRects):
    def select_best_position(self, width, height):
        """
        Search for the placement with the bes fitness for the rectangle.

        Returns:
            tuple (Rectangle, fitness) - Rectangle placed in the fittest position
            None - Rectangle couldn't be placed
        """
        if not self._max_rects:
            return None

        w, h = width, height
        # Normal rectangle
        fitn = ((self._rect_fitness(m, w, h), w, h, m) for m in self._max_rects
                if self._rect_fitness(m, w, h) is not None)
        fitn = [f for f in fitn]

        # Rotated rectangle
        fitr = ((self._rect_fitness(m, h, w), h, w, m) for m in self._max_rects
                if self._rect_fitness(m, h, w) is not None)
        fitr = [f for f in fitr]

        fit = fitr + fitn
        rectangles = []

        for _, w, h, m in fit:
            lower_left = (m.x, m.y)
            upper_left = (m.x, m.y + m.height - h)
            upper_right = (m.x + m.width - w, m.y)
            lower_right = (m.x + m.width - w, m.y + m.height - h)
            rectangles.append(Rectangle(upper_left[0], upper_left[1], w, h))
            rectangles.append(Rectangle(upper_right[0], upper_right[1], w, h))
            rectangles.append(Rectangle(lower_left[0], lower_left[1], w, h))
            rectangles.append(Rectangle(lower_right[0], lower_right[1], w, h))

        try:
            _, w, h, m = fit[0]
        except ValueError:
            return None

        rectangles = self._filter_out_candidates(rectangles)
        if not rectangles:
            return None

        return rectangles

    def _filter_out_candidates(self, candidates: list) -> list:
        """
        Filter out the candidates that are not suitable for the placement.

        Returns:
            list - List of candidates that are suitable for the placement
        """
        return [c for c in candidates if self._check_adjacent_rectangles(c) or self._check_rectangle_in_corner(c)]

    def _check_adjacent_rectangles(self, rect: Rectangle) -> bool:
        """
        Check if there are any adjacent rectangles to the given rectangle.

        Returns:
            bool - True if there are adjacent rectangles, False otherwise
        """
        for r in self.rectangles:
            print(r, rect)
            # check if left side of the rectangle is adjacent to the right side of the given rectangle, even partially
            if r.x + r.width == rect.x and r.y < rect.y + rect.height and r.y + r.height > rect.y:
                return True
            # check if right side of the rectangle is adjacent to the left side of the given rectangle, even partially
            if r.x == rect.x + rect.width and r.y < rect.y + rect.height and r.y + r.height > rect.y:
                return True
            # check if top side of the rectangle is adjacent to the bottom side of the given rectangle, even partially
            if r.y + r.height == rect.y and r.x < rect.x + rect.width and r.x + r.width > rect.x:
                return True
            # check if bottom side of the rectangle is adjacent to the top side of the given rectangle, even partially
            if r.y == rect.y + rect.height and r.x < rect.x + rect.width and r.x + r.width > rect.x:
                return True
        return False

    def _check_rectangle_in_corner(self, rect: Rectangle) -> bool:
        """
        Check if the rectangle is in the corner of the bin.

        Returns:
            bool - True if the rectangle is in the corner, False otherwise
        """
        if rect.x == 0 and rect.y == 0:
            return True
        if rect.x == 0 and rect.y == self.height - rect.height:
            return True
        if rect.x == self.width - rect.width and rect.y == 0:
            return True
        if rect.x == self.width - rect.width and rect.y == self.height - rect.height:
            return True
        return False


class CornerPointsSL(Skyline):
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
