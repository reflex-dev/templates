import json
import re
from typing import (
    List,
    Optional,
    Tuple,
    TypedDict,
)

import reflex as rx

_COLOR_CYCLE: List[Tuple[str, str]] = [
    ("bg-blue-500", "text-white"),
    ("bg-green-600", "text-white"),
    ("bg-red-500", "text-white"),
    ("bg-orange-500", "text-white"),
    ("bg-purple-500", "text-white"),
    ("bg-pink-500", "text-white"),
    ("bg-yellow-400", "text-black"),
    ("bg-teal-500", "text-white"),
    ("bg-cyan-500", "text-white"),
    ("bg-gray-600", "text-white"),
    ("bg-fuchsia-600", "text-white"),
    ("bg-lime-400", "text-black"),
    ("bg-rose-600", "text-white"),
    ("bg-amber-500", "text-black"),
    ("bg-indigo-700", "text-white"),
    ("bg-emerald-700", "text-white"),
    ("bg-sky-500", "text-white"),
]


class EntityInfo(TypedDict):
    name: str
    color: str
    text_color: str
    keywords: List[str]


class Segment(TypedDict):
    id: int
    text: str
    label_name: str
    bg_color: Optional[str]
    text_color: Optional[str]


class NerState(rx.State):
    """State for the Named Entity Recognition display."""

    _raw_text: str = 'Sia Kate Isobelle Furler (/\'siːə/ SEE-ə; born 18 December 1975) is an Australian singer, songwriter, record producer and music video director.[1] She started her career as a singer in the acid jazz band Crisp in the mid-1990s in Adelaide. In 1997, when Crisp disbanded, she released her debut studio album titled OnlySee in Australia. She moved to London, England, and provided lead vocals for the British duo Zero 7. In 2000, Sia released her second studio album, Healing Is Difficult, on the Columbia label the following year, and her third studio album, Colour the Small One, in 2004, but all of these struggled to connect with a mainstream audience. Sia relocated to New York City in 2005 and toured in the United States. Her fourth and fifth studio albums, Some People Have Real Problems and We Are Born, were released in 2008 and 2010, respectively. Each was certified gold by the Australian Recording Industry Association and attracted wider notice than her earlier albums. Uncomfortable with her growing fame, Sia took a hiatus from performing, during which she focused on songwriting for other artists, producing successful collaborations "Titanium" (with David Guetta), "Diamonds" (with Rihanna) and "Wild Ones" (with Flo Rida).'  # noqa: RUF001
    entities: List[EntityInfo] = [
        {
            "name": "PERSON",
            "color": "bg-blue-500",
            "text_color": "text-white",
            "keywords": [
                "Sia Kate Isobelle Furler",
                "Sia",
                "David Guetta",
                "Rihanna",
                "Flo Rida",
            ],
        },
        {
            "name": "COUNTRY",
            "color": "bg-green-600",
            "text_color": "text-white",
            "keywords": [
                "Australian",
                "Australia",
                "England",
                "United States",
            ],
        },
        {
            "name": "CITY",
            "color": "bg-red-500",
            "text_color": "text-white",
            "keywords": [
                "Adelaide",
                "London",
                "New York City",
            ],
        },
    ]
    display_segments: List[Segment] = []
    new_label_name: str = ""
    new_label_keywords_str: str = ""
    selected_label_name: Optional[str] = None
    available_colors: List[Tuple[str, str]] = _COLOR_CYCLE
    new_label_selected_color_index: int = 0
    _segment_id_counter: int = 0

    def _get_next_segment_id(self) -> int:
        self._segment_id_counter += 1
        return self._segment_id_counter

    def _reset_segment_ids(self):
        self._segment_id_counter = 0

    @rx.event
    def process_text_on_load(self):
        """Processes the raw text to identify and segment entities based on current labels."""
        self._reset_segment_ids()
        initial_parts = re.split("(\\s+|\\b)", self._raw_text)
        initial_segments: List[Segment] = [
            {
                "id": self._get_next_segment_id(),
                "text": part,
                "label_name": None,
                "bg_color": None,
                "text_color": None,
            }
            for part in initial_parts
            if part
        ]

        for entity in self.entities:
            for keyword in entity["keywords"]:
                keyword_segments = re.split("(\\s+|\\b)", keyword)
                keyword_words = [kw for kw in keyword_segments if kw and kw.strip()]
                if not keyword_words:
                    continue
                i = 0
                while i <= len(initial_segments) - len(keyword_words):
                    match = True
                    temp_indices = []
                    current_kw_idx = 0
                    current_seg_idx = i
                    while current_kw_idx < len(keyword_words):
                        while current_seg_idx < len(initial_segments) and (
                            not initial_segments[current_seg_idx]["text"].strip()
                        ):
                            current_seg_idx += 1
                        if current_seg_idx >= len(initial_segments):
                            match = False
                            break
                        if (
                            initial_segments[current_seg_idx]["text"]
                            != keyword_words[current_kw_idx]
                        ):
                            match = False
                            break
                        temp_indices.append(current_seg_idx)
                        current_kw_idx += 1
                        current_seg_idx += 1
                    if match:
                        applied_label = False
                        can_apply = all(
                            (
                                initial_segments[idx]["label_name"] is None
                                for idx in temp_indices
                            )
                        )
                        if can_apply:
                            for idx in temp_indices:
                                initial_segments[idx]["label_name"] = entity["name"]
                                initial_segments[idx]["bg_color"] = entity["color"]
                                initial_segments[idx]["text_color"] = entity[
                                    "text_color"
                                ]
                            applied_label = True
                        if applied_label:
                            i = temp_indices[-1] + 1
                        else:
                            next_word_idx = i + 1
                            while next_word_idx < len(initial_segments) and (
                                not initial_segments[next_word_idx]["text"].strip()
                            ):
                                next_word_idx += 1
                            i = next_word_idx
                    else:
                        next_word_idx = i + 1
                        while next_word_idx < len(initial_segments) and (
                            not initial_segments[next_word_idx]["text"].strip()
                        ):
                            next_word_idx += 1
                        i = next_word_idx
        self.display_segments = initial_segments
        self.selected_label_name = None

    @rx.event
    def select_label(self, label_name: Optional[str]):
        """Selects a label to apply or deselects if the same label is clicked again."""
        if self.selected_label_name == label_name:
            self.selected_label_name = None
        else:
            self.selected_label_name = label_name

    @rx.event
    def apply_label(self, segment_id: int):
        """Applies the selected label to the clicked segment or removes it."""
        if self.selected_label_name is None:
            return rx.toast("Select a label first!", duration=2000)
        target_segment_index = -1
        for i, seg in enumerate(self.display_segments):
            if seg["id"] == segment_id:
                target_segment_index = i
                break
        if target_segment_index == -1:
            return rx.toast("Segment not found.", duration=2000)
        if not self.display_segments[target_segment_index]["text"].strip():
            return
        selected_entity = None
        for entity in self.entities:
            if entity["name"] == self.selected_label_name:
                selected_entity = entity
                break
        if selected_entity:
            current_label = self.display_segments[target_segment_index]["label_name"]
            if current_label == self.selected_label_name:
                self.display_segments[target_segment_index]["label_name"] = None
                self.display_segments[target_segment_index]["bg_color"] = None
                self.display_segments[target_segment_index]["text_color"] = None
            else:
                self.display_segments[target_segment_index]["label_name"] = (
                    selected_entity["name"]
                )
                self.display_segments[target_segment_index]["bg_color"] = (
                    selected_entity["color"]
                )
                self.display_segments[target_segment_index]["text_color"] = (
                    selected_entity["text_color"]
                )
        else:
            return rx.toast(
                f"Label '{self.selected_label_name}' definition not found.",
                duration=3000,
            )

    @rx.event
    def set_new_label_name(self, name: str):
        """Updates the name for the new label being created."""
        self.new_label_name = name

    @rx.event
    def set_new_label_keywords_str(self, keywords: str):
        """Updates the keywords string for the new label being created."""
        self.new_label_keywords_str = keywords

    @rx.event
    def set_new_label_color_index(self, index: int):
        """Updates the selected color index for the new label."""
        self.new_label_selected_color_index = index

    @rx.event
    def add_new_label(self):
        """Adds a new label to the entities list using the selected color."""
        name = self.new_label_name.strip().upper()
        if not name:
            return rx.toast("Label name cannot be empty.", duration=3000)
        if any((entity["name"] == name for entity in self.entities)):
            return rx.toast(
                f"Label '{name}' already exists.",
                duration=3000,
            )
        keywords = [
            k.strip() for k in self.new_label_keywords_str.split(",") if k.strip()
        ]
        if not 0 <= self.new_label_selected_color_index < len(self.available_colors):
            self.new_label_selected_color_index = 0
        bg_color, text_color = self.available_colors[
            self.new_label_selected_color_index
        ]
        new_entity: EntityInfo = {
            "name": name,
            "color": bg_color,
            "text_color": text_color,
            "keywords": keywords,
        }
        self.entities.append(new_entity)
        self.new_label_name = ""
        self.new_label_keywords_str = ""
        self.new_label_selected_color_index = 0
        yield rx.toast(
            f"Label '{name}' added successfully.",
            duration=3000,
        )
        if keywords:
            yield NerState.process_text_on_load

    @rx.event
    def remove_label(self, label_name: str):
        """Removes a label definition and unlabels segments with that label."""
        self.entities = [
            entity for entity in self.entities if entity["name"] != label_name
        ]
        updated_segments = []
        for seg in self.display_segments:
            if seg["label_name"] == label_name:
                updated_segments.append(
                    {
                        **seg,
                        "label_name": None,
                        "bg_color": None,
                        "text_color": None,
                    }
                )
            else:
                updated_segments.append(seg)
        self.display_segments = updated_segments
        if self.selected_label_name == label_name:
            self.selected_label_name = None
        yield rx.toast(f"Label '{label_name}' removed.", duration=2000)

    @rx.var
    def annotated_text_json(self) -> str:
        """Creates a JSON string representation of the annotated text."""
        output_data = []
        current_entity_text = ""
        current_entity_label = None
        for segment in self.display_segments:
            if segment["label_name"] != current_entity_label:
                if current_entity_label and current_entity_text:
                    output_data.append(
                        {
                            "text": current_entity_text,
                            "label": current_entity_label,
                        }
                    )
                current_entity_text = segment["text"]
                current_entity_label = segment["label_name"]
            else:
                current_entity_text += segment["text"]
        if current_entity_label and current_entity_text:
            output_data.append(
                {
                    "text": current_entity_text,
                    "label": current_entity_label,
                }
            )
        elif not current_entity_label and current_entity_text:
            output_data.append({"text": current_entity_text, "label": None})
        final_output = []
        temp_text = ""
        for item in output_data:
            if item["label"] is None:
                temp_text += item["text"]
            else:
                if temp_text:
                    final_output.append({"text": temp_text, "label": None})
                    temp_text = ""
                final_output.append(item)
        if temp_text:
            final_output.append({"text": temp_text, "label": None})
        return json.dumps(
            {
                "annotations": final_output,
                "labels": self.entities,
            },
            indent=2,
        )
