import { Products } from './products';

export interface Vitrine {
  products_states: Products[];
  timestamp: string;
  vitrine_location: string;
}
