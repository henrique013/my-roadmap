export type PageType = 'roadmap' | 'node';

export type BlockType =
  | 'hero'
  | 'level_tabs'
  | 'node_grid'
  | 'concept_section'
  | 'source_list'
  | 'navigation_trail'
  | 'references';

export interface Source {
  id: string;
  title: string;
  url: string;
  source_type: string;
  reason: string;
  supports?: string[];
}

export interface NavigationLink {
  label: string;
  href: string;
  rel: string;
}

export interface PageBlock {
  id: string;
  type: BlockType;
  title?: string;
  text?: string;
  items?: Array<Record<string, unknown>>;
  props?: Record<string, unknown>;
}

export interface PageSpec {
  schema_version: string;
  page_type: PageType;
  title: string;
  slug: string;
  description: string;
  navigation?: NavigationLink[];
  blocks: PageBlock[];
  sources?: Source[];
}
